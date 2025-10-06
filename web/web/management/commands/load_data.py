import json
from django.core.management.base import BaseCommand
from django.conf import settings
from web.models import StartText, BotBlock, MediaFile, Callback


class Command(BaseCommand):
    help = "Загрузить данные из data.json в базу"

    def handle(self, *args, **options):
        path = settings.DATA_JSON
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            if "start_text" in item:
                StartText.objects.update_or_create(start_text=item["start_text"])
                self.stdout.write("Field start text updated")
                continue

            curr_callback, _ = Callback.objects.update_or_create(
                name=item["callback_data"]
            )

            on_callback = [
                Callback.objects.update_or_create(name=callback)[0]
                for callback in item.get("on_callback", [])
            ]

            media = [
                MediaFile.objects.create(file=file)
                for file in item.get("media", [])
            ]

            block = BotBlock.objects.create(
                button_name=item["button_name"],
                text=item["text"],
                callback_data=curr_callback,
            )

            block.on_callback.set(on_callback)
            block.media.set(media)

            self.stdout.write(f"Field {item['button_name']} updated")

        self.stdout.write("Done.")
