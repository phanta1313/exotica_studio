from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os


@staff_member_required  
def download_logs(request):
    file_path = settings.BASE_DIR / ".." / "logs/all_messages.csv"  
    file_path = os.path.abspath(file_path)           

    if not os.path.exists(file_path):
        return HttpResponse(f"Файл не найден ({file_path})", status=404)

    return FileResponse(open(file_path, "rb"), as_attachment=True, filename="all_messages.csv")

@staff_member_required  
def download_user_ids(request):
    file_path = settings.BASE_DIR / ".." / "logs/unique_users.csv"  
    file_path = os.path.abspath(file_path)           

    if not os.path.exists(file_path):
        return HttpResponse(f"Файл не найден ({file_path})", status=404)

    return FileResponse(open(file_path, "rb"), as_attachment=True, filename="unique_users.csv")