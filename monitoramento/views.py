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

            temp = data.get("temperatura")
            umid = data.get("umidade")
            vent = data.get("ventoinha")
            umidif = data.get("umidificador")

            LeituraSensor.objects.create(
                temperatura=temp,
                umidade=umid,
                ventoinha=vent,
                umidificador=umidif
            )

            return JsonResponse({
                "status": "salvo"
            })

        except Exception as e:

            print("ERRO:", e)

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

    dados = list(

        LeituraSensor.objects
        .order_by('-data')[:20]
        .values(
            'temperatura',
            'umidade',
            'ventoinha',
            'umidificador',
            'data'
        )
    )

    return JsonResponse(
        dados[::-1],
        safe=False
    )


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