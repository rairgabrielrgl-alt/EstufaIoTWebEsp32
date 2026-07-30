from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import timedelta
from .models import LeituraSensor
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import json
from django.shortcuts import render
from .models import LeituraSensor
from datetime import timedelta
from .models import EventoAcionamento

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

            leitura = LeituraSensor.objects.create(

                sensor=sensor,
                temperatura=temperatura,
                umidade=umidade,
                ventoinha=ventoinha,
                umidificador=umidificador,
                lampada=lampada

            )

            # Registrar eventos somente do sensor interno
            if sensor == "interno":

                for nome, estado in [

                    ("Peltier", leitura.ventoinha),
                    ("Umidificador", leitura.umidificador),
                    ("Lampada", leitura.lampada),

                ]:

                    ultimo = EventoAcionamento.objects.filter(
                        atuador=nome
                    ).order_by("-data").first()

                    if ultimo is None or ultimo.ligado != estado:

                        EventoAcionamento.objects.create(
                            atuador=nome,
                            ligado=estado
                        )

            return JsonResponse({
                "status": "salvo"
            })

        except Exception as e:

            print(e)

            return JsonResponse({
                "status": "erro",
                "mensagem": str(e)
            })

    return JsonResponse({
        "status": "metodo_invalido"
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

        dadoInterno = interno[tamanho - 1 - i]
        dadoExterno = externo[tamanho - 1 - i]

        lista.append({

            "temperatura_interna": dadoInterno.temperatura,
            "umidade_interna": dadoInterno.umidade,

            "temperatura_externa": dadoExterno.temperatura,
            "umidade_externa": dadoExterno.umidade,

            "ventoinha": dadoInterno.ventoinha,
            "umidificador": dadoInterno.umidificador,
            "lampada": dadoInterno.lampada,

            "data": dadoInterno.data

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



@login_required(login_url='/admin-login/')
def painel_admin(request):

    leituras = LeituraSensor.objects.order_by("data")

    acionamentos_peltier = 0
    acionamentos_umidificador = 0
    acionamentos_lampada = 0

    tempo_peltier = timedelta()
    tempo_umidificador = timedelta()
    tempo_lampada = timedelta()

    anterior = None

    for atual in leituras:

        if anterior:

            intervalo = atual.data - anterior.data

            # Tempo ligada
            if anterior.ventoinha:
                tempo_peltier += intervalo

            if anterior.umidificador:
                tempo_umidificador += intervalo

            if getattr(anterior, "lampada", False):
                tempo_lampada += intervalo

            # Contagem de acionamentos
            if not anterior.ventoinha and atual.ventoinha:
                acionamentos_peltier += 1

            if not anterior.umidificador and atual.umidificador:
                acionamentos_umidificador += 1

            if (not getattr(anterior, "lampada", False)
                    and getattr(atual, "lampada", False)):
                acionamentos_lampada += 1

        anterior = atual
    historico = (
    LeituraSensor.objects
    .filter(sensor="interno")
    .order_by("data")
    )    
    contexto = {

    "acionamentos_peltier": acionamentos_peltier,
    "acionamentos_umidificador": acionamentos_umidificador,
    "acionamentos_lampada": acionamentos_lampada,

    "tempo_peltier": tempo_peltier,
    "tempo_umidificador": tempo_umidificador,
    "tempo_lampada": tempo_lampada,

    "historico": historico,

        }
    

    historico = reversed(historico)

    return render(request,
                  "monitoramento/admin.html",
                  contexto)



def admin_login(request):

    if request.method == "POST":

        usuario = request.POST["usuario"]
        senha = request.POST["senha"]

        user = authenticate(
            request,
            username=usuario,
            password=senha
        )

        if user:

            login(request, user)
            return redirect("painel_admin")

    return render(request, "monitoramento/login.html")

