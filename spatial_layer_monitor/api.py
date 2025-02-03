import threading
import logging

from django.http import JsonResponse
from django.views import View
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsInOfficersGroup
from .tasks import run_check_all_layers

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsInOfficersGroup])
def mock_kmi_service(request):
    logger.info(request.data)
    logger.info(vars(request.POST))
    return JsonResponse({'message': 'Success'}, status=200)
    

@api_view(['POST'])
@permission_classes([IsInOfficersGroup])
def run_batch_import(request):
    x = threading.Thread(target=run_check_all_layers)
    x.run()
    return JsonResponse({'message': 'Success'}, status=200)
