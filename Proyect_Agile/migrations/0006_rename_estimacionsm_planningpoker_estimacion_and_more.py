# Generated by Django 4.1 on 2022-10-16 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0005_user_story_encargado_user_story_estimacion_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planningpoker',
            old_name='estimacionSM',
            new_name='estimacion',
        ),
        migrations.RemoveField(
            model_name='planningpoker',
            name='estimacionEncargado',
        ),
        migrations.RemoveField(
            model_name='planningpoker',
            name='estimacionFinal',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='BV',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='UP',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='estimacion',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='estimaciones',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='prioridad',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='tiempoDedicado',
        ),
        migrations.AddField(
            model_name='planningpoker',
            name='BV',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planningpoker',
            name='UP',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='planningpoker',
            name='prioridad',
            field=models.FloatField(),
        ),
    ]
