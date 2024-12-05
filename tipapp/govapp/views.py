"""Django project views."""


# Third-Party
import io
import os
import logging
from django import http
from django import shortcuts
from django.http import JsonResponse, HttpResponseForbidden, FileResponse
from django.views.generic import base
from django.contrib import auth
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from rest_framework.decorators import permission_classes, api_view
from rest_framework import views
from rest_framework.permissions import AllowAny
from .tasks import get_files_list, get_file_record, get_thermal_files, zip_thermal_file_or_folder


import json

# Internal
from govapp import settings

# Typing
from typing import Any

logger = logging.getLogger(__name__)

UserModel = auth.get_user_model()


class HomePage(base.TemplateView):
    """Home page view."""

    template_name = "govapp/home.html"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        context: dict[str, Any] = {}
        return shortcuts.render(request, self.template_name, context)   


class ThermalFilesDashboardView(base.TemplateView):
    """Thermal files view."""
    template_name = "govapp/thermal-files/dashboard.html"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        context: dict[str, Any] = {
            "route_path": settings.DATA_STORAGE
        }
        return shortcuts.render(request, self.template_name, context)

class ThermalFilesUploadView(base.TemplateView):
    """Thermal files upload."""

    # Template name
    template_name = "govapp/thermal-files/upload-files.html"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        # Construct Context
        pathToFolder = settings.PENDING_IMPORT_PATH
        context: dict[str, Any] = {}

        return shortcuts.render(request, self.template_name, context)


class UploadsHistoryView(base.TemplateView):
    """Thermal files uploaded after processing."""

    # Template name
    template_name = "govapp/thermal-files/uploads-history.html"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        # Construct Context
        context: dict[str, Any] = {
            "route_path": settings.UPLOADS_HISTORY_PATH
        }
        return shortcuts.render(request, self.template_name, context)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_pending_imports(request, *args, **kwargs):
    pathToFolder = settings.PENDING_IMPORT_PATH
    file_list = get_files_list(pathToFolder, ['.pdf', '.zip', '.7z'])
    page_param = request.GET.get('page', 1)
    page_size_param = request.GET.get('page_size', 10)
    paginator = Paginator(file_list, page_size_param)
    page = paginator.page(page_param)
   
    return JsonResponse({
        "count": paginator.count,
        "hasPrevious": page.has_previous(),
        "hasNext": page.has_next(),
        'results': page.object_list,
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def list_thermal_folder_contents(request, *args, **kwargs):
    dir_path = settings.DATA_STORAGE
    page_param = request.GET.get('page', '1')
    page_size_param = request.GET.get('page_size', '10')
    route_path = request.GET.get('route_path', '')
    search = request.GET.get('search', '')

    dir_path = route_path if route_path.startswith(dir_path) else os.path.join(dir_path, route_path)

    if not os.path.exists(dir_path):
        return JsonResponse({'error': f'Path [{dir_path}] does not exist.'}, status=400)

    file_list = get_thermal_files(dir_path, int(page_param) - 1, int(page_size_param), search)
    paginator = Paginator(file_list, page_size_param)
    page = paginator.page(page_param)
    return JsonResponse({
        "count": paginator.count,
        "hasPrevious": page.has_previous(),
        "hasNext": page.has_next(),
        'results': page.object_list,
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def list_uploads_history_contents(request, *args, **kwargs):
    dir_path = settings.UPLOADS_HISTORY_PATH
    page_param = request.GET.get('page', '1')
    page_size_param = request.GET.get('page_size', '10')
    route_path = request.GET.get('route_path', '')
    search = request.GET.get('search', '')

    dir_path = route_path if route_path.startswith(dir_path) else os.path.join(dir_path, route_path)

    if not os.path.exists(dir_path):
        return JsonResponse({'error': f'Path [{dir_path}] does not exist.'}, status=400)

    file_list = get_thermal_files(dir_path, int(page_param) - 1, int(page_size_param), search)
    paginator = Paginator(file_list, page_size_param)
    page = paginator.page(page_param)
    return JsonResponse({
        "count": paginator.count,
        "hasPrevious": page.has_previous(),
        "hasNext": page.has_next(),
        'results': page.object_list,
    })

@api_view(["POST"])
@permission_classes([AllowAny])
def api_upload_thermal_files(request, *args, **kwargs):
    if request.FILES:
        # uploaded_files = []  # Multiple files might be uploaded
        allowed_extensions = ['.zip', '.7z', '.pdf']
        uploaded_file = request.FILES.getlist('file')[0]
        newFileName = request.POST.get('newFileName', '')

        logger.info(f'File: [{uploaded_file.name}] is being uploaded...')

        # Check file extensions
        _, file_extension = os.path.splitext(uploaded_file.name)
        if file_extension.lower() not in allowed_extensions:
            return JsonResponse({'error': 'Invalid file type. Only .zip and .7z files are allowed.'}, status=400)

        # Save files
        save_path = os.path.join(settings.PENDING_IMPORT_PATH,  newFileName)
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        logger.info(f"File: [{uploaded_file.name}] has been successfully saved at [{save_path}].")
        file_info = get_file_record(settings.PENDING_IMPORT_PATH, newFileName)
        return JsonResponse({'message': 'File(s) uploaded successfully.', 'data' : file_info})
    else:
        logger.info(f"No file(s) were uploaded.")
        return JsonResponse({'error': 'No file(s) were uploaded.'}, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def api_delete_thermal_file(request, *args, **kwargs):
    file_name = request.data.get('newFileName', '')
    file_path = os.path.join(settings.PENDING_IMPORT_PATH, file_name)
    if file_name != '' and os.path.exists(file_path):
        os.remove(file_path)
        return JsonResponse({'message': f'File [{file_name}] has been deleted successfully.'})
    else:
        return JsonResponse({'error': f'File [{file_name}] does not exist.'}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_download_thermal_file_or_folder(request, *args, **kwargs):
    dir_path = settings.DATA_STORAGE
    file_path = request.GET.get('file_path', '')
    file_path = file_path if file_path.startswith(dir_path) else os.path.join(dir_path, file_path)
    
    if file_path != '' and os.path.exists(file_path):
        
        download_file_path = zip_thermal_file_or_folder(file_path)
        if download_file_path:
            filename = os.path.basename(download_file_path)
            zip_file = open(download_file_path, 'rb')
            return FileResponse(zip_file, as_attachment=True,  filename=filename)
    
    return JsonResponse({'error': f'There was an error with the download.'}, status=400)
    
