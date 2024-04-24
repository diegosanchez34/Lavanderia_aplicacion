from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

from app import views

urlpatterns = [
    path('', index, name='index'),
    path('listado/', listado, name="listado" ),
    path('lectura/', lectura, name="lectura" ),
    path('lectura_alerta/', lectura_alerta, name="lectura_alerta" ),
    path('lavado/', lavado, name="lavado" ),
    path('eliminar/', eliminar, name='eliminar'),
    path('ingreso/', ingreso, name='ingreso'),
    path('ingreso_alerta/<str:alerta>', ingreso_alerta, name='ingreso_alerta'),
    path('guardar/', guardar, name='guardar'),
    path('editar/', editar, name='editar'),
    path('actualizar/', actualizar, name='actualizar'),
    path('plantas/', plantas, name='plantas'),
    path('leer/', views.leer, name='leer'),
    path('leer_ingreso/', leer_ingreso, name='leer_ingreso'),
    path('exportar-a-excel/', exportar_a_excel, name='exportar_a_excel'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)