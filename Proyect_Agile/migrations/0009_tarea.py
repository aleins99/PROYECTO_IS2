# Generated by Django 3.2.12 on 2022-11-03 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Proyect_Agile', '0008_remove_user_story_encargado'),
    ]

    operations = [
        migrations.CreateModel(
            name='tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('descripcion', models.TextField()),
                ('idUs', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Proyect_Agile.user_story')),
            ],
        ),
    ]
