# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizacion', '0004_escuelacampo'),
        ('productores', '0003_auto_20160803_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produccioncacao',
            name='meses',
        ),
        migrations.AddField(
            model_name='entrevistados',
            name='escuela_campo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizacion.EscuelaCampo'),
        ),
        migrations.AlterField(
            model_name='certificacion',
            name='tipo',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Convencional'), (2, 'Org\xe1nico T1'), (3, 'Org\xe1nico T2'), (4, 'Org\xe1nico T3'), (5, 'Org\xe1nico Ecol\xf3gico'), (6, 'UTZ/Sello'), (7, 'Comercio Justo')], max_length=13, null=True, verbose_name='Tipo de certificaci\xf3n'),
        ),
        migrations.AlterField(
            model_name='plantacion',
            name='edad',
            field=models.IntegerField(choices=[(1, 'Menor de un a\xf1o'), (2, 'De 1 a 3 a\xf1os'), (3, 'De 4 a 10 a\xf1os'), (4, 'De 11 a 20 a\xf1os'), (5, 'Mayores de 20 a\xf1os')]),
        ),
        migrations.AlterField(
            model_name='produccioncacao',
            name='cacao_baba',
            field=models.FloatField(verbose_name='Producci\xf3n cacao en baba (lb baba/fresco)'),
        ),
    ]
