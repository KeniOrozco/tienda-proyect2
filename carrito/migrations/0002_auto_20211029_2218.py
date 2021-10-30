# Generated by Django 3.0.8 on 2021-10-30 04:18

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0001_initial'),
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
            field=models.CharField(default=datetime.datetime(2021, 10, 30, 4, 18, 18, 831580, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orden',
            name='estado_pago',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orden',
            name='no_guia',
            field=models.CharField(default=datetime.datetime(2021, 10, 30, 4, 18, 26, 571309, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orden',
            name='trasporte',
            field=models.IntegerField(choices=[(0, 'FORZA'), (1, 'GUATEX'), (2, 'CARGO')], default=0),
        ),
        migrations.AlterField(
            model_name='orden',
            name='direccion_entrega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orden_entrega', to='carrito.Direccion'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]