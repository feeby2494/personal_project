from django.urls import path
from .views import indexMap

urlpatterns = [
    path('', indexMap, name='route_map_home'),
]