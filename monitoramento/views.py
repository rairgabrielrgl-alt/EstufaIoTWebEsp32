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

            temperatura = data.get("temperatura")
            umidade = data.get("umidade")

            print("TEMP:", temperatura)
            print("UMID:", umidade)

            LeituraSensor.objects.create(
                temperatura=temperatura,
                umidade=umidade
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
        .values('temperatura', 'umidade', 'data')
    )

    return JsonResponse(dados[::-1], safe=False)
