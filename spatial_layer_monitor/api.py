import threading
import logging

from django.http import JsonResponse
from django.views import View
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view

from .tasks import run_check_all_layers

logger = logging.getLogger(__name__)

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
def mock_kmi_service(request):
    logger.info(request.data)
    logger.info(vars(request.POST))
    return JsonResponse({'message': 'Success'}, status=200)
    

@api_view(['POST'])
def run_batch_import(request):
    x = threading.Thread(target=run_check_all_layers)
    x.run()
    return JsonResponse({'message': 'Success'}, status=200)
