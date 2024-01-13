# Generated by Django 4.2.7 on 2024-01-04 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_presentacion_presentation_and_more'),
        ('consultations', '0011_alter_consultation_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='duracion',
        ),
        migrations.AddField(
            model_name='prescription',
            name='periodo',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Periodo (días)'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='periodo_indefinido',
            field=models.BooleanField(default=False, verbose_name='Periodo Indefinido'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='costo',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Costo de la Consulta'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='consultations.consultation', verbose_name='Consulta Relacionada'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='dosis',
            field=models.PositiveIntegerField(verbose_name='Dosis'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='frecuencia',
            field=models.CharField(max_length=2, verbose_name='Frecuencia'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='indicaciones',
            field=models.TextField(blank=True, null=True, verbose_name='Indicaciones Adicionales'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Producto'),
        ),
    ]