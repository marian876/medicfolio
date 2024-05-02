# Generated by Django 4.2.7 on 2024-01-22 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_careprofile_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestpatient',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado'), ('finalizado', 'Finalizado')], default='pendiente', max_length=10),
        ),
    ]