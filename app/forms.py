from django import forms
from .models import Pechera
from .models import Lavado

class FormPechera(forms.ModelForm):
    class Meta:
        model = Pechera
        fields = ['id_pechera', 'fecha_fabricacion', 'talla', 'cantidad_lavados', 'observaciones', 'planta', 'parameters', 'indice_microbiologico']
        
        widgets = {
            'id_pechera': forms.TextInput(attrs={'readonly': 'readonly'}),  # Hacer que el campo sea de solo lectura
            'fecha_fabricacion': forms.DateInput(attrs={'type': 'date'}),
        }
        


class FiltroPecheraForm(forms.Form):
    id_pechera = forms.CharField(max_length=100, label='ID de Pechera')