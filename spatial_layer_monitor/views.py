import threading
import urllib3
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
import urllib3.contrib
import urllib3.util
from urllib import parse


from .tasks import run_check_all_layers
from .models import SpatialMonitor, RequestAuthentication

# Home
class AddSpatialLayerInfo(View):
    # Main page for adding spatial layer information
    template_name = 'spatial_layer_monitor/add_spatial_layer_info.html'

    def get(self, request, *args, **kwargs):

        auth_modes = RequestAuthentication.objects.all().only('id', 'name','username',  'created_at')

        context = {
            'title': 'Add Spatial Layer Information',
            'auth_modes': auth_modes,
            'success': request.GET.get('success') == 'True'
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        urls = request.POST.getlist('layer_url')
        auth_mode = request.POST.get('auth_mode')
        authentication = None
        if auth_mode != '':
            RequestAuthentication.objects.filter(pk=auth_mode).first()
        for url in urls:
            urlObj = parse.urlparse(url)
            params  = parse.parse_qs(urlObj.query)

            name = params['layer'][0] if 'layer' in params else urlObj.path

            SpatialMonitor.objects.get_or_create( defaults={'name': name}, url=url, authentication=authentication,)     

        return redirect('/?success=True')
