"""Spatial Layer Monitor Management Command."""


# Third-Party
import os
import logging
import subprocess
from django.core.management import base
from datetime import datetime
# Local
from spatial_layer_monitor import settings
from spatial_layer_monitor.queue_processor import QueueProcessor
logger = logging.getLogger(__name__)


class Command(base.BaseCommand):
    """Read Spatial Layers Monitor Command."""
    # Help string
    help = "Processes Spatial Layers Monitor"  # noqa: A003

    def handle(self, *args, **kwargs) -> None:
        """Handles the management command functionality."""
        # Display information
        self.stdout.write("Processing imported files...")
        QueueProcessor().publish_changed_layers()

        
        

