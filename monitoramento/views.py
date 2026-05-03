from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import LeituraSensor
import json
from django.shortcuts import render

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

            return JsonResponse({"status": "salvo"})

        except Exception as e:
            print("ERRO:", e)
            return JsonResponse({"status": "erro"})

    return JsonResponse({"status": "erro"})

def painel(request):
    dados = LeituraSensor.objects.all().order_by('-data')[:10]  # Últimas 10 leituras

    return render(request, 'monitoramento/painel.html', {"status": "ok", "dados": dados})



def api_dados(request):
    dados = list(
        LeituraSensor.objects.order_by('-data')[:20]
        .values('temperatura', 'umidade', 'ventoinha', 'umidificador', 'data')
    )

    return JsonResponse(dados[::-1], safe=False)

from django.contrib.auth.models import User

def criar_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@email.com', '123456')
    return JsonResponse({'status': 'ok'})

estado_umidificador = "off"

def controle(request):
    global estado_umidificador

    if request.method == "POST":
        estado_umidificador = request.POST.get("umidificador")

    return JsonResponse({"status": estado_umidificador})    

def estado(request):
 return JsonResponse({"umidificador": estado_umidificador})
