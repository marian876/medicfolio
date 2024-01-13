# Generated by Django 4.2.7 on 2024-01-02 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_rename_presentacion_presentation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(verbose_name='Fecha y Hora')),
                ('acompanante', models.CharField(blank=True, max_length=255, null=True, verbose_name='Acompañante')),
                ('pedido_estudios', models.TextField(blank=True, verbose_name='Pedido de Estudios')),
                ('notas', models.TextField(blank=True, verbose_name='Notas')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre del Médico')),
                ('especialidad', models.CharField(max_length=255, verbose_name='Especialidad')),
                ('telefono_personal', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono Personal')),
                ('ubicacion_consultorio1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ubicación Consultorio 1')),
                ('telefono_reservas1', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono Reservas 1')),
                ('ubicacion_consultorio2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ubicación Consultorio 2')),
                ('telefono_reservas2', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono Reservas 2')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='doctores/', verbose_name='Imagen')),
                ('notas', models.TextField(blank=True, verbose_name='Notas')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosis', models.TextField(verbose_name='Dosis')),
                ('instrucciones', models.TextField(verbose_name='Instrucciones')),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recetas', to='consultations.appointment', verbose_name='Cita')),
                ('medicamentos', models.ManyToManyField(to='products.product', verbose_name='Medicamentos')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultations.doctor', verbose_name='Médico'),
        ),
    ]