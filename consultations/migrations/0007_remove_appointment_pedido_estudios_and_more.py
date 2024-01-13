# Generated by Django 4.2.7 on 2024-01-03 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0006_alter_appointment_options_remove_prescription_dosis_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='pedido_estudios',
        ),
        migrations.AddField(
            model_name='appointment',
            name='cita_posterior',
            field=models.BooleanField(default=False, verbose_name='Cita Posterior'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='estudios',
            field=models.BooleanField(default=False, verbose_name='Estudios'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='medicamentos',
            field=models.BooleanField(default=False, verbose_name='Medicamentos'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='otras_indicaciones',
            field=models.BooleanField(default=False, verbose_name='Otras Indicaciones'),
        ),
    ]