from django.db.models import Q

from django.db import models
from django_cryptography.fields import encrypt
from datetime import datetime
class RequestAuthentication(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=200)
    password =  encrypt(models.CharField(max_length=512, blank=True, default=""))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.username


class SpatialMonitor(models.Model):
    url = models.URLField(max_length=1000)
    name = models.CharField(max_length=200)
    destination_url = models.URLField(blank=True, null=True, max_length=1000)
    description = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    last_checked = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    authentication = models.ForeignKey(RequestAuthentication, on_delete=models.CASCADE, blank=True, null=True)

    def get_latest_hash(self):
        return self.hashes.all().order_by('created_at').first()
    
    def get_authentication(self):
        if self.authentication:
            return (self.authentication.username, self.authentication.password)
        return None

    def __str__(self):
        return self.name

class SpatialMonitorHistory(models.Model):
    layer = models.ForeignKey(SpatialMonitor, on_delete=models.CASCADE, related_name='hashes')
    hash = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at =  models.DateTimeField(blank=True, null=True)

    def sync(self):
        self.synced_at = datetime.now()
        self.layer.last_updated = datetime.now()
        self.layer.save()
        self.save()

    def __str__(self):
        return f'{self.layer.name} - {self.hash} - {self.created_at}'


class SpatialQueue(models.Model):
    layer = models.ForeignKey(SpatialMonitorHistory, on_delete=models.CASCADE, related_name='queue_item')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.layer.layer.name} - {self.created_at}'

