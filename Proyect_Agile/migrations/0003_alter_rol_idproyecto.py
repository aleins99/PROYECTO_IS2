# Generated by Django 4.1 on 2022-09-27 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0002_tipous_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='idProyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.proyecto'),
        ),
    ]
