from django.contrib import admin
from .models import BotBlock, MediaFile, StartText, Callback

class MediaFileInline(admin.TabularInline):
    model = BotBlock.media.through 
    extra = 1
    verbose_name = "Медиа файл"
    verbose_name_plural = "Медиа файлы"

@admin.register(BotBlock)
class BotBlockAdmin(admin.ModelAdmin):
    inlines = [MediaFileInline]
    exclude = ("media",) 
    list_display = ("button_name", "text")


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("file",)


@admin.register(StartText)
class StartTextAdmin(admin.ModelAdmin):
    list_display = ("start_text",)


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ("name",)
