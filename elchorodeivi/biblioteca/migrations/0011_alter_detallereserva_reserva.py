# Generated by Django 5.0.6 on 2024-07-09 01:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0010_alter_detallereserva_reserva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallereserva',
            name='reserva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.reserva'),
        ),
    ]
