# Generated by Django 4.2.7 on 2024-01-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_familyprofile_parentezco_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='careprofile',
            name='comentario',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Comentarios'),
        ),
        migrations.AddField(
            model_name='careprofile',
            name='disponibilidad',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Disponibilidad'),
        ),
        migrations.AddField(
            model_name='careprofile',
            name='recomendacion',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Recomendado por'),
        ),
    ]
