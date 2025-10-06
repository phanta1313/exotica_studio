from django.db import models
from django.core.exceptions import ValidationError


class Callback(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Callback данные'
        verbose_name_plural = 'Callback данные'

    def __str__(self):
        return self.name


class BotBlock(models.Model):
    button_name = models.CharField(max_length=255, blank=True, null=True,unique=True, verbose_name="Название кнопки")
    text = models.TextField(blank=True, null=True, verbose_name="Текст")
    callback_data = models.ForeignKey(Callback, related_name="callback_data", on_delete=models.CASCADE, verbose_name="callback данные")
    media = models.ManyToManyField("MediaFile", blank=True, verbose_name="Медиафайл")
    on_callback = models.ManyToManyField(Callback, blank=True, related_name="on_callback", verbose_name="хэндлер callback данных")

    class Meta:
        verbose_name = 'Кнопка'
        verbose_name_plural = 'Кнопки'

    def __str__(self):
        return self.button_name or f"Block {self.id}"


class MediaFile(models.Model):
    file = models.FileField(upload_to="")

    class Meta:
        verbose_name = 'Медиафайл'
        verbose_name_plural = 'Медиафайлы'

    def __str__(self):
        return self.file.name


class StartText(models.Model):
    start_text = models.TextField(blank=True, null=True, verbose_name="Начальный текст")  

    class Meta:
        verbose_name = 'Начальный текст'
        verbose_name_plural = 'Начальный текст'

    def clean(self):
        if StartText.objects.exists() and not self.pk:
            raise ValidationError("Можно создать только один объект с начальным текстом")
    
    def __str__(self):
        return self.start_text[0:10] + "..."