# Generated by Django 4.2.7 on 2024-01-16 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_requestpatient_aceptada_requestpatient_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('celular', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('experiencia', models.TextField(default='', verbose_name='Experiencia laboral')),
                ('habilidades', models.TextField(default='', verbose_name='Habilidades')),
                ('educacion', models.TextField(default='', verbose_name='Educación')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil de Cuidador',
                'verbose_name_plural': 'Perfiles de Cuidadores',
            },
        ),
        migrations.CreateModel(
            name='FamilyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parentezco', models.TextField(default='', verbose_name='Parentezco')),
                ('celular', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('cohabitacion', models.BooleanField(default=False, verbose_name='Cohabitación')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil de Familiar',
                'verbose_name_plural': 'Perfiles de Familiares',
            },
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('celular', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('historial', models.TextField(default='', verbose_name='Historial')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('alergias', models.TextField(default='No especificado', verbose_name='Alergias')),
                ('enfermedades_base', models.TextField(default='', verbose_name='Enfermedades de base')),
                ('cirugias', models.TextField(default='', verbose_name='Cirugías')),
                ('enfermedades_familiares', models.TextField(default='', verbose_name='Enfermedades familiares')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('encargado', models.ForeignKey(limit_choices_to={'groups__name': 'Familiar'}, on_delete=django.db.models.deletion.CASCADE, related_name='patients', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Perfil de Paciente',
                'verbose_name_plural': 'Perfiles de Pacientes',
            },
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
