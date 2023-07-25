from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

default_urls = DefaultRouter()

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(default_urls.urls)),
    path('', include('djoser.urls')),
]