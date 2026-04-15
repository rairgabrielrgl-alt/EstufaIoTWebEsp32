from django.urls import path
from . import views

urlpatterns = [
    path('dados/', views.receber_dados),
    path('painel/', views.painel),
    path('api/', views.api_dados),
]
