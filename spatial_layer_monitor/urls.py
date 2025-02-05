"""
URL configuration for layerCacheService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django import conf
from django import urls
from . import api as layerCacheService_views
from . import views


admin.site.site_header = conf.settings.PROJECT_TITLE
admin.site.index_title = conf.settings.PROJECT_TITLE
admin.site.site_title = conf.settings.PROJECT_TITLE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('run_batch_import/', layerCacheService_views.run_batch_import, name='run_batch_import'),

    urls.path('', views.HomeView.as_view(), name='home'),
    urls.path('dashboard', views.HistoryDataInfoView.as_view(), name='dashboard'),
    urls.path('add-records', views.AddSpatialLayerInfoView.as_view(), name='add-records'),
    urls.path('api/list_historical_records/', views.list_historical_records),
]
