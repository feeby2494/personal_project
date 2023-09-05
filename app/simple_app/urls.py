from django.urls import path
from app.simple_app import views

urlpatterns = [
    path('', views.index, name='simple_app_home'),
    path('bingo/', views.bingo, name='bingo'),
    path('bmi/', views.bmi, name='bmi')
]