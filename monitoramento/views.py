from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import LeituraSensor

import json


# =========================================
# RECEBER DADOS DO ESP32
# =========================================

@csrf_exempt
def receber_dados(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            sensor = data.get("sensor")

            temperatura = data.get("temperatura")

            umidade = data.get("umidade")

            ventoinha = data.get("ventoinha", False)

            umidificador = data.get("umidificador", False)

            lampada = data.get("lampada", False)
            LeituraSensor.objects.create(

                sensor=sensor,

                temperatura=temperatura,

                umidade=umidade,

                ventoinha=ventoinha,

                umidificador=umidificador

                lampada=lampada

            )

            return JsonResponse({

                "status": "salvo"

            })

        except Exception as e:

            print(e)

            return JsonResponse({

                "status": "erro"

            })

    return JsonResponse({

        "status": "erro"

    })

# =========================================
# PAINEL
# =========================================

def painel(request):

    dados = (
        LeituraSensor.objects
        .all()
        .order_by('-data')[:10]
    )

    return render(
        request,
        'monitoramento/painel.html',
        {
            "status": "ok",
            "dados": dados
        }
    )


# =========================================
# API DOS DADOS
# =========================================

def api_dados(request):

    interno = (
        LeituraSensor.objects
        .filter(sensor="interno")
        .order_by("-data")[:30]
    )

    externo = (
        LeituraSensor.objects
        .filter(sensor="externo")
        .order_by("-data")[:30]
    )

    tamanho = min(len(interno), len(externo))

    lista = []

    for i in range(tamanho):

        lista.append({

            "temperatura_interna": interno[tamanho-1-i].temperatura,
            "umidade_interna": interno[tamanho-1-i].umidade,

            "temperatura_externa": externo[tamanho-1-i].temperatura,
            "umidade_externa": externo[tamanho-1-i].umidade,

            "ventoinha": interno[tamanho-1-i].ventoinha,
            "umidificador": interno[tamanho-1-i].umidificador,

            "data": interno[tamanho-1-i].data

        })

    return JsonResponse(lista, safe=False)


# =========================================
# CRIAR ADMIN
# =========================================

def criar_admin(request):

    if not User.objects.filter(username='admin').exists():

        User.objects.create_superuser(
            'admin',
            'admin@email.com',
            '123456'
        )

    return JsonResponse({
        'status': 'ok'
    })


# =========================================
# CONTROLE DO UMIDIFICADOR
# =========================================

estado_umidificador = "off"


def controle(request):

    global estado_umidificador

    if request.method == "POST":

        estado_umidificador = request.POST.get(
            "umidificador"
        )

        return JsonResponse({
            "status": estado_umidificador
        })

    return JsonResponse({
        "status": estado_umidificador
    })


# =========================================
# ESTADO ATUAL
# =========================================

def estado(request):

    return JsonResponse({
        "umidificador": estado_umidificador
    })