# Generated by Django 3.0.8 on 2021-10-22 21:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0002_auto_20211022_2104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orden',
            options={'verbose_name_plural': 'Orden'},
        ),
        migrations.AlterModelOptions(
            name='ordenitem',
            options={'verbose_name_plural': 'Orden de items'},
        ),
        migrations.RemoveField(
            model_name='direccion',
            name='pais',
        ),
        migrations.RemoveField(
            model_name='direccion',
            name='region',
        ),
        migrations.AddField(
            model_name='direccion',
            name='departamento',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]