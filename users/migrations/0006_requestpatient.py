# Generated by Django 4.2.7 on 2024-01-15 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aceptada', models.BooleanField(default=False)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_recibidas', to=settings.AUTH_USER_MODEL)),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_enviadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]