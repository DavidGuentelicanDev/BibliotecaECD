# Generated by Django 5.0.6 on 2024-07-06 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0003_libro_portada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='anio_edicion',
        ),
        migrations.RemoveField(
            model_name='libro',
            name='otros_autores',
        ),
        migrations.RemoveField(
            model_name='libro',
            name='pais_edicion',
        ),
        migrations.AlterField(
            model_name='libro',
            name='autor',
            field=models.CharField(max_length=100),
        ),
    ]