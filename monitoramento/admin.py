from django.contrib import admin
from .models import LeituraSensor
from .models import LeituraSensor, EventoAcionamento
admin.site.register(LeituraSensor)
admin.site.register(EventoAcionamento)
