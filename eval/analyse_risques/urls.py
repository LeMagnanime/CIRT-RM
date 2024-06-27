from django.urls import path
from . import views


urlpatterns = [
    path('home2', views.home2, name='home2'),
    path('vulnerabilite', views.vulnerabilite, name='vulnerabilite'),
    path('exemple', views.exemple, name='exemple'),
    path('essaie', views.essaie, name='essaie'),
    path('api/get_gpt_response/', views.get_gpt_response, name='get_gpt_response'), 
    path('registre/', views.registre_risque, name='registre_risque'),
] 