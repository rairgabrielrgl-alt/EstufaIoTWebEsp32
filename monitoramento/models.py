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


class EventoAcionamento(models.Model):

    ATUADORES = [
        ("Peltier", "Peltier"),
        ("Umidificador", "Umidificador"),
        ("Lampada", "Lampada"),
    ]

    atuador = models.CharField(max_length=20, choices=ATUADORES)

    ligado = models.BooleanField()

    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data"]

    def __str__(self):

        estado = "Ligou" if self.ligado else "Desligou"

        return f"{self.atuador} - {estado} - {self.data.strftime('%d/%m/%Y %H:%M:%S')}"