from django.db import models

class RegistroPonto(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('folga', 'Folga'),
        ('atestado', 'Atestado'),
    ]
    mes = models.IntegerField()
    dia = models.IntegerField()
    ano = models.IntegerField()
    entrada = models.TimeField(null=True, blank=True)
    inicio_intervalo = models.TimeField(null=True, blank=True)
    fim_intervalo = models.TimeField(null=True, blank=True)
    saida = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='normal')

    def __str__(self):
        return f"{self.dia:02d}/{self.mes:02d}/{self.ano}- {self.status}"

    class Meta:
        unique_together = ('ano', 'mes', 'dia')
        ordering = ['ano', 'mes', 'dia']

