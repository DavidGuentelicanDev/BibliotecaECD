# Generated by Django 5.0.6 on 2024-07-08 06:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0008_alter_reserva_fec_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fec_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
