from django.db import models

class LeituraSensor(models.Model):

    # Sensor interno
    temperatura_interna = models.FloatField()
    umidade_interna = models.FloatField()

    # Sensor externo
    temperatura_externa = models.FloatField()
    umidade_externa = models.FloatField()

    # Atuadores
    ventoinha = models.BooleanField(default=False)
    umidificador = models.BooleanField(default=False)

    # Data da leitura
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Interno: {self.temperatura_interna}°C / {self.umidade_interna}% | "
            f"Externo: {self.temperatura_externa}°C / {self.umidade_externa}% | "
            f"Vent: {'ON' if self.ventoinha else 'OFF'} | "
            f"Umidif: {'ON' if self.umidificador else 'OFF'} | "
            f"{self.data.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    
    