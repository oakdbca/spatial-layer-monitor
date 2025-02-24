from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import status
import urllib3.contrib
import urllib3.util
from urllib import parse
import mimetypes

from django.http.response import HttpResponse
from .models import SpatialMonitor, RequestAuthentication, SpatialMonitorHistory
from .permissions import IsInOfficersGroup, IsAdministratorMixin
from .serializers import SpatialMonitorHistorySerializer

# Home
class AddSpatialLayerInfoView(IsAdministratorMixin, View):
    # Main page for adding spatial layer information
    template_name = 'spatial_layer_monitor/add_spatial_layer_info.html'

    def get(self, request, *args, **kwargs):

        auth_modes = RequestAuthentication.objects.all().only('id', 'name','username', 'created_at')
        has_error = request.GET.get('error') == 'True'
        context = {
            'title': 'Add Spatial Layer Information',
            'auth_modes': auth_modes,
            'success': request.GET.get('success') == 'True',
            'error_message': 'An error occurred' if has_error else None,
            'has_permission': IsInOfficersGroup().has_permission(request, self),
        }

        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        urls = request.POST.getlist('layer_url')
        layer_name = request.POST.getlist('layer_name')
        auth_mode = request.POST.get('auth_mode')

        if not IsInOfficersGroup().has_permission(request, self):
            return redirect('/?error=True')

        authentication = None
        if auth_mode != '':
            authentication = RequestAuthentication.objects.filter(pk=auth_mode).first()
        for (x, url) in enumerate(urls):
            urlObj = parse.urlparse(url)
            params  = parse.parse_qs(urlObj.query)

            name = params['layer'][0] if 'layer' in params else urlObj.path

            SpatialMonitor.objects.get_or_create( defaults={'name': name}, url=url, authentication=authentication, kmi_layer_name=layer_name[x])     

        return redirect('/?success=True')

class HomeView(IsAdministratorMixin, View):
    template_name = 'spatial_layer_monitor/view_history_data.html'
    def get(self, request, *args, **kwargs):
        return redirect('dashboard')

class HistoryDataInfoView(IsAdministratorMixin, View):
    # Main page for adding spatial layer information
    template_name = 'spatial_layer_monitor/view_history_data.html'

    def get(self, request, *args, **kwargs):         
        context = {
            'has_permission': IsInOfficersGroup().has_permission(request, self),
        }

        return render(request, self.template_name, context=context)
    
@api_view(["GET"])
@permission_classes([IsInOfficersGroup])
def list_historical_records(request, *args, **kwargs):
    
    page_param = request.GET.get('page', '1')
    page_size_param = request.GET.get('page_size', '10')
    
    search = request.GET.get('search', '')

    file_list = SpatialMonitorHistory.objects.all().order_by("-id").select_related("layer")
    paginator = Paginator(file_list, page_size_param)
    page = paginator.page(page_param)
    return JsonResponse({
        "count": paginator.count,
        "hasPrevious": page.has_previous(),
        "hasNext": page.has_next(),
        'results': SpatialMonitorHistorySerializer(page.object_list, many=True).data,
    })



@api_view(['GET'])
@permission_classes([IsInOfficersGroup])
def get_file(request, id, rest,extension):
    map_file = get_object_or_404(SpatialMonitorHistory, id=id)
    file = map_file.image
    if file is None:
        return HttpResponse("File doesn't exist", status=status.HTTP_404_NOT_FOUND)

    file_data = None
    with open(file.path, 'rb') as f:
         file_data = f.read()
         f.close()
    return HttpResponse(file_data, content_type=mimetypes.types_map['.'+str(extension)])