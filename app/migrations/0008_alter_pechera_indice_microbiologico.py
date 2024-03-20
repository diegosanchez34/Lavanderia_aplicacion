# Generated by Django 4.2.6 on 2023-10-30 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_pechera_indice_microbiologico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pechera',
            name='indice_microbiologico',
            field=models.CharField(choices=[('Sí', 'Sí'), ('No', 'No')], default='si', max_length=2, verbose_name='Índice Microbiológico'),
        ),
    ]