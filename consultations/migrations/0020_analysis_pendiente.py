# Generated by Django 4.2.7 on 2024-01-06 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0019_alter_analysis_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='pendiente',
            field=models.BooleanField(default=True, verbose_name='Pendiente'),
        ),
    ]
