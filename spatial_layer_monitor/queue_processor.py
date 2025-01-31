

# Third-Party
import os
import logging
import subprocess
from datetime import datetime
# Local
from spatial_layer_monitor import settings
from .models import SpatialQueue, SpatialMonitorHistory
from .tasks import post_layer_update

from django.conf import settings

logger = logging.getLogger(__name__)

class QueueProcessor():

    def __init__(self):
        pass

    def publish_changed_layers(self):
        logger.info(f"Processing pending Layers found")
        try:
            queue_items = SpatialQueue.objects.all().select_related('layer__layer')
            for queue_item in queue_items:
                layer = queue_item.layer
                logger.info(f"Processing Layer: {layer.layer.id}")
                try:
                    kmiUrl = settings.KMI_UPDATE_URL
                    if not kmiUrl:
                        logger.info(f"Layer {layer.layer.id} has no destination URL")
                        continue
                    success, result = post_layer_update(kmiUrl, auth=layer.layer.get_authentication(), data={})
                    logger.info(result)
                    if success:
                        layer.sync()
                        queue_item.delete()
                        
                except Exception as e:
                    logger.error(e)
        except Exception as e:
            logger.error(e)
