from django.urls import path
from .views import indexSocial

urlpatterns = [
    path('', indexSocial, name='social_network_home'),
]