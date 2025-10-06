from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
