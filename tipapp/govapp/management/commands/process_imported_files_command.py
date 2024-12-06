"""Thermal Image Processing Management Command."""


# Third-Party
import os
import logging
import subprocess
from django.core.management import base
from datetime import datetime
# Local
from govapp import settings
from govapp.imports_processor import ImportsProcessor
logger = logging.getLogger(__name__)


class Command(base.BaseCommand):
    """Read Imported Thermal Files Command."""
    # Help string
    help = "Processes Imported Thermal Files"  # noqa: A003

    def handle(self, *args, **kwargs) -> None:
        """Handles the management command functionality."""
        # Display information
        self.stdout.write("Processing imported files...")
        ImportsProcessor(settings.PENDING_IMPORT_PATH, settings.UPLOADS_HISTORY_PATH).process_files()

        
        

