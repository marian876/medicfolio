# Generated by Django 4.2.7 on 2024-01-17 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_careprofile_familyprofile_patientprofile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careprofile',
            name='celular',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='careprofile',
            name='educacion',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Educación'),
        ),
        migrations.AlterField(
            model_name='careprofile',
            name='experiencia',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Experiencia laboral'),
        ),
        migrations.AlterField(
            model_name='careprofile',
            name='habilidades',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Habilidades'),
        ),
        migrations.AlterField(
            model_name='familyprofile',
            name='celular',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='familyprofile',
            name='cohabitacion',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Cohabitación'),
        ),
        migrations.AlterField(
            model_name='familyprofile',
            name='parentezco',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Parentezco'),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='alergias',
            field=models.TextField(blank=True, default='No especificado', null=True, verbose_name='Alergias'),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='cirugias',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Cirugías'),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='enfermedades_base',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Enfermedades de base'),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='enfermedades_familiares',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Enfermedades familiares'),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='historial',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Historial'),
        ),
    ]