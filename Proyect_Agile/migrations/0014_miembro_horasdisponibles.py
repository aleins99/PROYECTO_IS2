# Generated by Django 4.1 on 2022-11-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0013_alter_user_story_estimacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='horasDisponibles',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]