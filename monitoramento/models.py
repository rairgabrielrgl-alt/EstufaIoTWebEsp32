from django.db import models

class LeituraSensor(models.Model):
    temperatura = models.FloatField()
    umidade = models.FloatField()
    ventoinha = models.BooleanField(default=False)
    umidificador = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temp: {self.temperatura}°C, Umid: {self.umidade}%, Vent: {'ON' if self.ventoinha else 'OFF'}, Umidif: {'ON' if self.umidificador else 'OFF'} - {self.data.strftime('%Y-%m-%d %H:%M:%S')}"  



