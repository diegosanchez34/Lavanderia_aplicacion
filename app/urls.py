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
    path('registro/', registro, name='registro'),
    path('ingreso/', ingreso, name='ingreso'),
    path('guardar/', guardar, name='guardar'),
    path('editar/', editar, name='editar'),
    path('actualizar/', actualizar, name='actualizar'),
    path('plantas/', plantas, name='plantas'),
    path('leer-rfid/', views.leer_rfid, name='leer_rfid'),
    path('leer/', views.leer, name='leer'),
    path('registro/<str:rfid_data>/', views.registro_con_uid, name='registro_con_uid'),
    path('exportar-a-excel/', exportar_a_excel, name='exportar_a_excel'),
    path('post-registro/<str:rfid_data>/', post_registro, name="post-registro"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)