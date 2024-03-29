# Generated by Django 4.2.7 on 2024-01-17 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0022_alter_prescription_producto'),
        ('users', '0009_alter_careprofile_celular_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='medico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='consultations.doctor', verbose_name='Médico'),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='seguro',
            field=models.TextField(blank=True, null=True, verbose_name='Seguro médico'),
        ),
    ]
