
from rest_framework import serializers
from .models import SpatialMonitor, SpatialMonitorHistory

class SpatialMonitorHistorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="layer.name")
    layer_name = serializers.CharField(source="layer.kmi_layer_name")
    layer_id = serializers.CharField(source="layer.id")

    class Meta:
        model = SpatialMonitorHistory
        fields = "__all__"


