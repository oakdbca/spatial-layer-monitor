from django.contrib import admin
from .models import SpatialMonitor, SpatialMonitorHistory, SpatialQueue, RequestAuthentication


class SpatialMonitorHistoryInline(admin.TabularInline):
    model = SpatialMonitorHistory
    extra = 0
    exclude = ['wkb_geometry',]


@admin.register(SpatialMonitor)
class SpatialMonitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'kmi_layer_name', 'url', 'last_checked', 'created_at', 'authentication')
    list_filter = ('last_checked', 'created_at', 'authentication')
    search_fields = ('name', 'url')
    inlines = [SpatialMonitorHistoryInline]

@admin.register(SpatialMonitorHistory)
class SpatialMonitorHistoryAdmin(admin.ModelAdmin):
    list_display = ('layer', 'hash', 'created_at', 'synced_at')
    list_filter = ('created_at', 'synced_at')
    search_fields = ('layer', 'hash')


@admin.register(RequestAuthentication)
class RequestAuthenticationAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'username')

    fields = ('name', 'username', 'password', 'description')

    def password(self, obj):
        return '*** CLASSIFIED *** {}'.format(obj.password)

    

admin.site.register(SpatialQueue)
