import json
from django.conf import settings
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import BotBlock, StartText


def dump_data_to_json():
    data = []

    # Добавляем стартовый текст
    start = StartText.objects.first()
    if start:
        data.append({"start_text": start.start_text})

    # Добавляем все блоки
    for block in BotBlock.objects.all():
        btn_data = {
            "button_name": block.button_name,
            "text": block.text,
            "media": [m.file.name for m in block.media.all()],
            "callback_data": block.callback_data.name if block.callback_data else None,
            "on_callback": list(block.on_callback.values_list("name", flat=True)),
        }
        data.append(btn_data)

    # Безопасная запись в JSON
    try:
        with open(settings.DATA_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[dump_data_to_json] Ошибка при записи JSON: {e}")


# --- Сигналы ---

@receiver(post_save, sender=BotBlock)
@receiver(post_delete, sender=BotBlock)
@receiver(post_save, sender=StartText)
@receiver(post_delete, sender=StartText)
def update_json(sender, instance, **kwargs):
    dump_data_to_json()


@receiver(m2m_changed, sender=BotBlock.media.through)
@receiver(m2m_changed, sender=BotBlock.on_callback.through)
def update_json_m2m(sender, instance, **kwargs):
    # Чтобы не писать в JSON на каждой промежуточной операции (add/remove)
    if kwargs.get("action") in ["post_add", "post_remove", "post_clear"]:
        dump_data_to_json()
