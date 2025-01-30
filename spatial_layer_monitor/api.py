import threading

from django.http import JsonResponse
from django.views import View
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view

from .tasks import run_check_all_layers

class LayerCacheView(View):
    def get(self, request, *args, **kwargs):
        layer_url = request.GET.get('layer_url')
        if layer_url:
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'error': 'layer_url parameter is required'}, status=400)
        
'''
     TODO: Implement batch import of layers
        - 

'''
@api_view(['POST'])
def run_batch_import(request):
    pass

@api_view(['POST'])
def run_batch_import(request):
    x = threading.Thread(target=run_check_all_layers)
    x.run()
    return JsonResponse({'message': 'Success'}, status=200)
