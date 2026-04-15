from django.db import models

class LeituraSensor(models.Model):
    temperatura = models.FloatField()
    umidade = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

class Controle(models.Model):
    ventoinha = models.BooleanField(default=False)    