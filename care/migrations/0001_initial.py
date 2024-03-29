# Generated by Django 4.2.7 on 2024-01-15 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsable', models.CharField(choices=[('familiar', 'Familiar'), ('cuidador', 'Cuidador'), ('enfermera', 'Enfermera')], max_length=100)),
                ('nombre', models.TextField(blank=True, null=True)),
                ('lugar', models.CharField(choices=[('casa', 'Casa'), ('sanatorio', 'Sanatorio'), ('consulta', 'Consulta'), ('salida', 'Salida')], max_length=100)),
                ('inicio_asignado', models.DateTimeField()),
                ('fin_asignado', models.DateTimeField()),
                ('inicio_real', models.DateTimeField()),
                ('fin_real', models.DateTimeField()),
                ('recordatorio', models.TextField(blank=True, null=True)),
                ('informe', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
