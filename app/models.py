from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# se crea modelo para pecheras

PARAMETERS_CHOICES = [
    ('1', 'Nuevo'),
    ('2', 'Perfectas condiciones'),
    ('3', 'Ligermante desgastanda'),
    ('4', 'Desgastada'),
]

PLANTAS_CHOICES = [
    (1, 'Sin asignar'),
    (2, 'ABICK S.A'),
    (3, 'CONTINENTALES SPA'),
    (4, 'CUTTER S.A'),
    (5, 'OCEAN BLUE SPA'),
    (6, 'PESQUERA DEL MAR ANTARTICO S.A'),
    (7, 'PROCESOS FILETES DEL SUR SPA'),
    (8, 'RIO YELCHO SPA'),
    (9, 'RIO BLANCO'),
]

OPCIONES_INDICE = [
    ('Si', 'Si'),
    ('No', 'No'),
]

class Pechera(models.Model):
    id_pechera = models.CharField(max_length=100, unique=True)
    fecha_fabricacion = models.DateField(null=True)
    talla = models.CharField(max_length=5)
    cantidad_lavados = models.IntegerField(default=0)
    observaciones = models.CharField(max_length=500, blank=True)
    planta = models.IntegerField (choices=PLANTAS_CHOICES,default=1)
    parameters = models.CharField(max_length=50, choices=PARAMETERS_CHOICES, default='1')
    indice_microbiologico = models.CharField(max_length=2, choices=OPCIONES_INDICE, default='Si', verbose_name="Índice Microbiológico")
    eliminada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id_pechera} {'(Eliminada)' if self.eliminada else ''}"

class Lavado(models.Model):
    id_lavado = models.AutoField(primary_key=True, unique=True)
    id_pechera = models.CharField(max_length=100,null=True)
    fecha_lavado = models.DateField(null=True)

class Planta(models.Model):
    id_planta = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=50,null=True)
    cantidad = models.IntegerField (default=0)
    kilos = models.IntegerField (default=0)
