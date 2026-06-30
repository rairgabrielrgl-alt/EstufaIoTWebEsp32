from django.urls import path
from . import views

urlpatterns = [
    # recebe dados do ESP32
    path('dados/', views.receber_dados, name='receber_dados'),

    # painel web
    path('painel/', views.painel, name='painel'),

    # API para o gráfico
    path('api/', views.api_dados, name='api_dados'),

    # controle do umidificador
    path('controle/', views.controle, name='controle'),

    # estado atual
    path('estado/', views.estado, name='estado'),
]