# views.py
from django.shortcuts import render, redirect
from .models import Pechera
from .models import Lavado
from .forms import *
import serial
from .forms import FormPechera, FiltroPecheraForm
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, datetime
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# Create your views here.


from .models import Pechera

def index(request):
    # Obtén las últimas pecheras (por ejemplo, las últimas 20) ordenadas por fecha de fabricación descendente
    latest_pecheras = Pechera.objects.exclude(eliminada=True).order_by('-fecha_fabricacion')[:10]

    # Calcula la cantidad de pecheras fabricadas el último año
    today = datetime.now()
    last_year = today - timedelta(days=365)
    manufactured_last_year = Pechera.objects.filter(fecha_fabricacion__gte=last_year).count()

    # Calcular la cantidad de pecheras fabricadas el último mes
    last_month = today - timedelta(days=30)
    manufactured_last_month = Pechera.objects.filter(fecha_fabricacion__gte=last_month).count()

    # Pecheras lavadas
    washed_last_month = Pechera.objects.filter(cantidad_lavados__gte=1, fecha_fabricacion__gte=last_month, fecha_fabricacion__lte=today).count()

    # Pecheras defectuosas del último mes
    faulty_last_month = Pechera.objects.filter(eliminada=True, fecha_fabricacion__gte=last_month).count()

    # Pecheras disponibles
    disponibles = Pechera.objects.filter(planta__icontains='Planta0',eliminada=False).count()

    # Pecheras en planta
    planta = Pechera.objects.exclude(planta__iexact='Planta0',eliminada=False).count()

    context = {
        'latest_pecheras': latest_pecheras,
        'manufactured_last_year': manufactured_last_year,
        'manufactured_last_month': manufactured_last_month,
        'faulty_last_month': faulty_last_month,
        'washed_last_month': washed_last_month,
        'disponibles': disponibles,
        'planta': planta,
    }

    return render(request, 'app/index.html', context)


def registro(request):
    error_message = None
    rfid_data = request.POST.get('rfid_data')

    if request.method == 'POST':
        form = FormPechera(request.POST)
        if form.is_valid():
            # Guardar los datos en la base de datos
            form.save()
            return redirect('index')
        else:
            error_message = "Hubo un error al guardar los datos"
    else:
        form = FormPechera(initial={'id_pechera': rfid_data})

    return render(request, 'app/registro.html', {'form': form, 'error_message': error_message, 'rfid_data': rfid_data})

def ingreso(request):   
    pechera = None  # Inicialmente, no se muestra ninguna pechera
    if request.method == 'GET':
        id_pechera = request.GET.get("id")
        pechera = Pechera.objects.filter(id_pechera=id_pechera).first()

    planta_choices = [
    ('Planta0', 'Sin asignar'),
    ('Planta1', 'ABICK S.A'),
    ('Planta2', 'CONTINENTALES SPA'),
    ('Planta3', 'CUTTER S.A'),
    ('Planta4', 'OCEAN BLUE SPA'),
    ('Planta5', 'PESQUERA DEL MAR ANTARTICO S.A'),
    ('Planta6', 'PROCESOS FILETES DEL SUR SPA'),
    ('Planta7', 'RIO YELCHO SPA'),
    ('Planta8', 'RIO BLANCO'),]

    parameters_choices = [
    ('1', 'Nuevo'),
    ('2', 'Perfectas condiciones'),
    ('3', 'Ligermante desgastanda'),
    ('4', 'Desgastada'),]

    opciones_indice = [('Si'),('No'),]
    context = {'pechera': pechera, 'planta_choices': planta_choices, 'parameters_choices': parameters_choices,'opciones_indice': opciones_indice}
    return render(request, 'app/ingreso.html', context)

def guardar(request):
    alerta = "Error al intentar ingresar la pechera"
    return render(request, 'app/ingreso.html',  {'alerta':alerta})

def editar(request):
    pechera = None
    
    if request.method == 'GET':
        id_pechera = request.GET.get("id")
        pechera = Pechera.objects.filter(id_pechera=id_pechera).first()

    planta_choices = [
    ('Planta0', 'Sin asignar'),
    ('Planta1', 'ABICK S.A'),
    ('Planta2', 'CONTINENTALES SPA'),
    ('Planta3', 'CUTTER S.A'),
    ('Planta4', 'OCEAN BLUE SPA'),
    ('Planta5', 'PESQUERA DEL MAR ANTARTICO S.A'),
    ('Planta6', 'PROCESOS FILETES DEL SUR SPA'),
    ('Planta7', 'RIO YELCHO SPA'),
    ('Planta8', 'RIO BLANCO'),]

    parameters_choices = [
    ('1', 'Nuevo'),
    ('2', 'Perfectas condiciones'),
    ('3', 'Ligermante desgastanda'),
    ('4', 'Desgastada'),]

    opciones_indice = [('Si'),('No'),]
    context = {'pechera': pechera, 'planta_choices': planta_choices, 'parameters_choices': parameters_choices,'opciones_indice': opciones_indice}
    return render(request, 'app/editar.html', context)

def actualizar(request):
    pechera = Pechera.objects.filter(id_pechera=request.POST['id_pechera']).first()
    if pechera:
        pechera.id_pechera = request.POST['id_pechera']
        pechera.fecha_fabricacion = request.POST['fecha_fabricacion']
        pechera.talla = request.POST['talla']
        pechera.cantidad_lavados = request.POST['cantidad_lavados']
        pechera.observaciones = request.POST['observaciones']
        pechera.planta = request.POST['planta']
        pechera.parameters = request.POST['parameters']
        pechera.indice_microbiologico = request.POST['indice_microbiologico']
        pechera.save()
    else:
        print("No se encontró la pechera con el UID especificado")
    return HttpResponseRedirect(f"/lectura?id={pechera.id_pechera}")

def listado(request):
    # Obtener todas las pecheras ordenadas por fecha de fabricación descendente
    latest_pecheras = Pechera.objects.exclude(eliminada=True).order_by('-fecha_fabricacion')[:]

    planta_choices = [
    ('Planta0', 'Sin asignar'),
    ('Planta1', 'ABICK S.A'),
    ('Planta2', 'CONTINENTALES SPA'),
    ('Planta3', 'CUTTER S.A'),
    ('Planta4', 'OCEAN BLUE SPA'),
    ('Planta5', 'PESQUERA DEL MAR ANTARTICO S.A'),
    ('Planta6', 'PROCESOS FILETES DEL SUR SPA'),
    ('Planta7', 'RIO YELCHO SPA'),
    ('Planta8', 'RIO BLANCO'),]

    context = {
        'latest_pecheras': latest_pecheras,'planta_choices': planta_choices
    }

    return render(request, 'app/listado.html', context)

def plantas(request):
    # Obtener todas las pecheras ordenadas por fecha de fabricación descendente
    latest_pecheras = Pechera.objects.exclude(eliminada=True).order_by('-fecha_fabricacion')[:]

    # Contar las pecheras por planta
    abick = Pechera.objects.filter(planta__icontains='Planta1',eliminada=False).count()
    continentales = Pechera.objects.filter(planta__icontains='Planta2',eliminada=False).count()
    cutter = Pechera.objects.filter(planta__icontains='Planta3',eliminada=False).count()
    ocean = Pechera.objects.filter(planta__icontains='Planta4',eliminada=False).count()
    antartico = Pechera.objects.filter(planta__icontains='Planta5',eliminada=False).count()
    filetes = Pechera.objects.filter(planta__icontains='Planta6',eliminada=False).count()
    yelcho = Pechera.objects.filter(planta__icontains='Planta7',eliminada=False).count()
    blanco = Pechera.objects.filter(planta__icontains='Planta8',eliminada=False).count()

    #calcular kg de plastico
    kg_abick = (abick*150)/1000
    kg_continentales = (continentales*150)/1000
    kg_cutter = (cutter*150)/1000
    kg_ocean = (ocean*150)/1000
    kg_antartico = (antartico*150)/1000
    kg_filetes = (filetes*150)/1000
    kg_yelcho = (yelcho*150)/1000
    kg_blanco = (blanco*150)/1000

    context = {
        'latest_pecheras': latest_pecheras,
        'abick': abick,
        'continentales': continentales,
        'cutter': cutter,
        'ocean': ocean,
        'antartico': antartico,
        'filetes': filetes,
        'yelcho': yelcho,
        'blanco': blanco,
        'kg_abick' : kg_abick,
        'kg_continentales' : kg_continentales,
        'kg_cutter' : kg_cutter,
        'kg_ocean' : kg_ocean,
        'kg_antartico' : kg_antartico,
        'kg_filetes' : kg_filetes,
        'kg_yelcho' : kg_yelcho,
        'kg_blanco' : kg_blanco
    }

    return render(request, 'app/plantas.html', context)

def leer_rfid(request):
    arduino_port = 'COM4'
    baud_rate = 9600
    arduino = None

    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        while True:
            rfid_data_full = arduino.readline().decode().strip()
            # Verificar si el valor es "Listo para leer etiquetas RFID..."
            if rfid_data_full != "Listo para leer etiquetas RFID...":
                # Extraer el UID eliminando el texto no deseado
                prefix = "Número de serie de la tarjeta RFID:"
                if rfid_data_full.startswith(prefix):
                    rfid_data = rfid_data_full[len(prefix):].strip().replace(" ", "")
                else:
                    rfid_data = rfid_data_full.replace(" ", "")

                if rfid_data:
                    print("RFID TAG: ", rfid_data)

                    # Verificar si el UID ya existe en la base de datos
                    existing_pechera = Pechera.objects.filter(id_pechera=rfid_data).first()
                    if existing_pechera:
                        print("UID ya existe en la base de datos")

                        # Incrementar el campo cantidad_lavados en 1
                        existing_pechera.cantidad_lavados += 1
                        existing_pechera.save()

                        print("cantidad_lavados incrementado a:", existing_pechera.cantidad_lavados)

                        # Redirigir a la vista de post-registro
                        return redirect('post-registro', rfid_data=rfid_data)
                    else:
                        # Guardar el UID en la base de datos
                        Pechera.objects.create(id_pechera=rfid_data)
                        print("UID guardado en la base de datos")

                        # Redirigir a la vista de registro_con_uid con el UID leído
                        return redirect('registro_con_uid', rfid_data=rfid_data)

    except KeyboardInterrupt:
        print("Lectura de RFID detenida.")
    except Exception as e:
        print("Error: ", e)
    finally:
        if arduino is not None:
            arduino.close()

    return HttpResponse("Lectura RFID completada.")


def registro_con_uid(request, rfid_data):
    pechera = Pechera.objects.filter(id_pechera=rfid_data).first()

    if pechera:
        # Si el UID existe, redirige a la vista de post-registro
        return redirect('post-registro', rfid_data=rfid_data)
    else:
        # Si el UID no existe, muestra el formulario de registro con el UID
        if request.method == 'POST':
            form = FormPechera(request.POST, instance=pechera)
            if form.is_valid():
                form.save()  # Guarda los datos modificados o crea un nuevo registro si es necesario
                return redirect('index')
        else:
            form = FormPechera(instance=pechera, initial={'id_pechera': rfid_data})

        return render(request, 'app/registro.html', {'form': form, 'rfid_data': rfid_data})


def exportar_a_excel(request):
    # Obtén los datos de la base de datos
    pecheras = Pechera.objects.all()
  
    # Crea un nuevo libro de Excel
    wb = Workbook()
    ws = wb.active

    # Agrega encabezados a las columnas
    ws['A1'] = 'ID de Pechera'
    ws['B1'] = 'Planta'
    ws['C1'] = 'Fecha de Fabricación'
    ws['D1'] = 'Cantidad de Lavados'
    ws['E1'] = 'Talla'
    ws['F1'] = 'Observaciones'
    ws['G1'] = 'Parámetros'
    ws['H1'] = 'Índice Microbiológico'

    # Aplica estilos a los encabezados
    for cell in ws['1:1']:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
        cell.fill = PatternFill(start_color='FFD700', end_color='FFD700', fill_type='solid')

    # Aplica bordes a los encabezados
    for row in ws.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.border = Border(bottom=Side(style='thin'))

    # Llena las filas con los datos de la base de datos
    row = 2
    for pechera in pecheras:
        ws.cell(row=row, column=1, value=pechera.id_pechera)
        ws.cell(row=row, column=2, value=pechera.get_planta_display())
        ws.cell(row=row, column=3, value=pechera.fecha_fabricacion.strftime('%Y-%m-%d'))
        ws.cell(row=row, column=4, value=pechera.cantidad_lavados)
        ws.cell(row=row, column=5, value=pechera.talla)
        ws.cell(row=row, column=6, value=pechera.observaciones)
        ws.cell(row=row, column=7, value=pechera.get_parameters_display())
        ws.cell(row=row, column=8, value=pechera.indice_microbiologico)

        # Aplica estilos a las celdas
        for cell in ws[row]:
            cell.alignment = Alignment(horizontal='center')

        row += 1

    # Ajusta el ancho de las columnas para que se ajusten al contenido
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width

    # Crea una respuesta HTTP con el libro de Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="pecheras.xlsx"'
    wb.save(response)

    return response

def post_registro(request, rfid_data=None):
    pechera = None

    if rfid_data:
        # Si se proporciona un RFID, intenta encontrar el registro correspondiente
        pechera = Pechera.objects.filter(id_pechera=rfid_data).first()

    if request.method == 'POST':
        form = FormPechera(request.POST, instance=pechera)
        if form.is_valid():
            # Actualiza el campo eliminada si la opción es 'Eliminar'
            if form.cleaned_data['parameters'] == '5':
                form.instance.eliminada = True
            form.save()  # Guarda los datos modificados o crea un nuevo registro si es necesario
            return redirect('index')
    else:
        form = FormPechera(instance=pechera, initial={'id_pechera': rfid_data})

    return render(request, 'app/post-registro.html', {'form': form})


def lectura(request):   
    pechera = None  # Inicialmente, no se muestra ninguna pechera
    lista_lavados = None  # Inicialmente, no se muestra ninguna pechera
    if request.method == 'GET':
        id_pechera = request.GET.get("id")
        pechera = Pechera.objects.filter(id_pechera=id_pechera).first()
        lista_lavados = Lavado.objects.filter(id_pechera=id_pechera)[:]

    context = {'pechera': pechera, "lista_lavados":lista_lavados}

    return render(request, 'app/lectura.html', context)

def lavado(request):    
    pechera = None  # Inicialmente, no se muestra ninguna pechera
    if request.method == 'POST':
        form = FiltroPecheraForm(request.POST)
        if form.is_valid():
            id_pechera = form.cleaned_data['id_pechera']
            pechera = Pechera.objects.filter(id_pechera=id_pechera).first()
    else:
        form = FiltroPecheraForm()

    context = {
        'form': form,
        'pechera': pechera
    }

    return render(request, 'app/lavado.html', context)

def eliminar(request):    
    pechera = None  # Inicialmente, no se muestra ninguna pechera
    if request.method == 'POST':
        form = FiltroPecheraForm(request.POST)
        if form.is_valid():
            id_pechera = form.cleaned_data['id_pechera']
            pechera = Pechera.objects.filter(id_pechera=id_pechera).first()
    else:
        form = FiltroPecheraForm()

    context = {
        'form': form,
        'pechera': pechera
    }

    return render(request, 'app/eliminar.html', context)
