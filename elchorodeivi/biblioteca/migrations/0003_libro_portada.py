# Generated by Django 5.0.6 on 2024-07-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0002_alter_usuario_comuna_alter_usuario_direccion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='portada',
            field=models.ImageField(blank=True, null=True, upload_to='assets/'),
        ),
    ]
