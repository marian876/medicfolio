# Generated by Django 4.2.7 on 2024-01-26 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_compra_creado_el_compra_creado_por'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='creado_el',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
