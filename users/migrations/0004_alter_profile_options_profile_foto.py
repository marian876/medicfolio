# Generated by Django 4.2.7 on 2024-01-13 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_options_remove_profile_apellido_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Perfil', 'verbose_name_plural': 'Perfiles'},
        ),
        migrations.AddField(
            model_name='profile',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
