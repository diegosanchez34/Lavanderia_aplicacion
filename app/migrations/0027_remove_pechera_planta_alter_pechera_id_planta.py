# Generated by Django 5.0.2 on 2024-04-23 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_pechera_id_planta_alter_pechera_planta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pechera',
            name='planta',
        ),
        migrations.AlterField(
            model_name='pechera',
            name='id_planta',
            field=models.IntegerField(choices=[(1, 'Sin asignar'), (2, 'ABICK S.A'), (3, 'CONTINENTALES SPA'), (4, 'CUTTER S.A'), (5, 'OCEAN BLUE SPA'), (6, 'PESQUERA DEL MAR ANTARTICO S.A'), (7, 'PROCESOS FILETES DEL SUR SPA'), (8, 'RIO YELCHO SPA'), (9, 'RIO BLANCO')], default=1),
        ),
    ]