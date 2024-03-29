# Generated by Django 4.1 on 2022-11-04 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0010_tarea_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planningpoker',
            name='BV',
        ),
        migrations.RemoveField(
            model_name='planningpoker',
            name='UP',
        ),
        migrations.RemoveField(
            model_name='planningpoker',
            name='miembroEncargado',
        ),
        migrations.RemoveField(
            model_name='planningpoker',
            name='prioridad',
        ),
        migrations.AddField(
            model_name='user_story',
            name='BV',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_story',
            name='UP',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_story',
            name='miembroEncargado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.miembro'),
        ),
        migrations.AddField(
            model_name='user_story',
            name='prioridad',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
