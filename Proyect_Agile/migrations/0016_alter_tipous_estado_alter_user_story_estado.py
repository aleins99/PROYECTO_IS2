# Generated by Django 4.1 on 2022-11-24 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0015_auto_20221124_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipous',
            name='estado',
            field=models.TextField(default='Por hacer, En Proceso, Hecho, Finalizado'),
        ),
        migrations.AlterField(
            model_name='user_story',
            name='estado',
            field=models.CharField(default='N', max_length=30),
        ),
    ]