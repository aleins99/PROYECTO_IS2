# Generated by Django 4.1 on 2022-09-26 19:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0003_alter_tipous_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipous',
            name='estado',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('N', 'Nuevo'), ('PP', 'En Planning Pocker'), ('P', 'Pendiente'), ('EP', 'En Proceso'), ('STSA', 'Sin Terminar Sprint Anterior'), ('A', 'Aprobado'), ('H', 'Hecho'), ('C', 'Cancelado')], default='N', max_length=4), default=list, size=None),
        ),
    ]
