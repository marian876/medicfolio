# Generated by Django 4.2.7 on 2024-01-24 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0003_product_paciente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_asociados', to=settings.AUTH_USER_MODEL, verbose_name='Paciente'),
        ),
    ]
