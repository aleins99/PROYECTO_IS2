# Generated by Django 4.1 on 2022-09-08 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Proyect_Agile', '0005_remove_proyecto_usbacklog_remove_proyecto_miembros_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miembro',
            name='correo',
        ),
        migrations.AddField(
            model_name='miembro',
            name='idproyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.proyecto'),
        ),
        migrations.AddField(
            model_name='miembro',
            name='idrol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.rol'),
        ),
        migrations.AddField(
            model_name='miembro',
            name='isActivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='miembro',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='scrumMaster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]