# Generated by Django 4.1 on 2022-09-03 03:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(choices=[('P', 'Pendiente'), ('E', 'En ejecucion'), ('C', 'Cancelado'), ('F', 'Finalizado')], default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fechafin',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fechainicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('id_proyectos', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.proyecto')),
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
                ('descripcion', models.TextField()),
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
                ('idProyecto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargahoraria', models.IntegerField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='scrumMaster',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.usuario'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='usbacklog',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.user_story'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='miembros',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.miembro'),
        ),
    ]