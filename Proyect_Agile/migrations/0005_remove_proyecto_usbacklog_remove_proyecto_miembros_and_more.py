# Generated by Django 4.1 on 2022-09-06 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0004_remove_miembro_usuario_miembro_correo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='usbacklog',
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='miembros',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='miembros',
            field=models.ManyToManyField(to='Proyect_Agile.miembro'),
        ),
    ]