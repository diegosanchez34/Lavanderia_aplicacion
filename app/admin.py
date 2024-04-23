from django.contrib import admin

from app.models import Pechera
from app.models import Lavado
from app.models import Planta

# Register your models here.

admin.site.register(Pechera)
admin.site.register(Lavado)
admin.site.register(Planta)