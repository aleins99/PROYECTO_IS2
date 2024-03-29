# Generated by Django 4.1 on 2022-09-26 04:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargahoraria', models.IntegerField(default=0)),
                ('isActivo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, max_length=200, null=True)),
                ('fechainicio', models.DateField(default=datetime.datetime.now)),
                ('fechafin', models.DateField()),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('E', 'En ejecucion'), ('C', 'Cancelado'), ('F', 'Finalizado')], default='P', max_length=1)),
                ('miembros', models.ManyToManyField(to='Proyect_Agile.miembro')),
                ('scrumMaster', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User_Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('comentarios', models.TextField()),
                ('estimaciones', models.IntegerField()),
                ('historial', models.TextField()),
                ('UP', models.IntegerField()),
                ('BV', models.IntegerField()),
                ('estado', models.CharField(default='N', max_length=10)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.tipous')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('agregarUserStory', models.BooleanField(default=False)),
                ('eliminarUserStory', models.BooleanField(default=False)),
                ('modificarUserStory', models.BooleanField(default=False)),
                ('agregarMiembro', models.BooleanField(default=False)),
                ('modificarMiembro', models.BooleanField(default=False)),
                ('eliminarMiembro', models.BooleanField(default=False)),
                ('crearRol', models.BooleanField(default=False)),
                ('modificarRol', models.BooleanField(default=False)),
                ('eliminarRol', models.BooleanField(default=False)),
                ('crearSprint', models.BooleanField(default=False)),
                ('empezarSprint', models.BooleanField(default=False)),
                ('finalizarSprint', models.BooleanField(default=False)),
                ('agregarSprintBacklog', models.BooleanField(default=False)),
                ('modificarSprintBacklog', models.BooleanField(default=False)),
                ('idProyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.proyecto')),
            ],
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
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tipous',
            name='estado',
            field=models.TextField(default='Por hacer, En Proceso, Hecho, Cancelado'),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('fechainicio', models.DateField(default=datetime.datetime.now)),
                ('fechafin', models.DateField()),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('E', 'En ejecucion'), ('F', 'Finalizado')], default='P', max_length=1)),
                ('idproyecto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.proyecto')),
            ],
        ),
        migrations.AddField(
            model_name='tipous',
            name='idproyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.proyecto')
        ),

        migrations.AddField(
            model_name='user_story',
            name='idproyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT,
                                    to='Proyect_Agile.proyecto'),
        ),
        migrations.AlterField(
            model_name='user_story',
            name='estado',
            field=models.CharField(default='Pendiente', max_length=30),
        ),
    ]
