from django.db import models


class LeituraSensor(models.Model):

    SENSOR_CHOICES = (
        ('interno', 'Interno'),
        ('externo', 'Externo'),
    )

    sensor = models.CharField(max_length=10, choices=SENSOR_CHOICES)

    temperatura = models.FloatField()

    umidade = models.FloatField()

    ventoinha = models.BooleanField(default=False)

    umidificador = models.BooleanField(default=False)
    lampada = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"{self.sensor} | "
            f"{self.temperatura}°C | "
            f"{self.umidade}%"
        )