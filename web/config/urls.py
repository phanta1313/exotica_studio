from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from web import views
from django.http import HttpResponse
from django.shortcuts import redirect


def redirect_admin(request):
    return redirect("/admin")

urlpatterns = [
    path('', redirect_admin),
    path('admin/', admin.site.urls),
    path('download-logs/', views.download_logs, name='скачать логи'),
    path('download-user-ids/', views.download_user_ids, name='скачать ID пользователей'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)


