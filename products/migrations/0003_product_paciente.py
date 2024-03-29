# Generated by Django 4.2.7 on 2024-01-24 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_rename_presentacion_presentation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='paciente',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='productos_paciente', to=settings.AUTH_USER_MODEL, verbose_name='Paciente'),
            preserve_default=False,
        ),
    ]
