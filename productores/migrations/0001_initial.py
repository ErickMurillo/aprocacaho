# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-16 14:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lugar', '0003_auto_20150804_1931'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaFinca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.FloatField(verbose_name='3.1 \xc1rea total en manzanas que tiene la propiedad')),
            ],
            options={
                'verbose_name': '3 Uso de la Tierra',
                'verbose_name_plural': '3 Uso de la Tierra',
            },
        ),
        migrations.CreateModel(
            name='DetalleAreaFinca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seleccion', models.IntegerField(choices=[(1, 'Bosque'), (2, 'Tacotal o regeneraci\xf3n natural'), (3, 'Cultivo anual ( que produce en el a\xf1o)'), (4, 'Plantaci\xf3n forestal ( madera y le\xf1a)'), (5, '\xc1rea de pastos abierto'), (6, '\xc1rea de pastos con \xe1rboles'), (7, 'Cultivo perenne (frutales)'), (8, 'Cultivo semi-perenne (mus\xe1cea, pi\xf1a)'), (9, 'Solo destinado para cacao'), (10, 'Huerto mixto con cacao'), (11, 'Otros')], verbose_name='3.2 Distribuci\xf3n de la finca')),
                ('area', models.FloatField()),
            ],
            options={
                'verbose_name': '3 Uso de la Tierra',
                'verbose_name_plural': '3 Uso de la Tierra',
            },
        ),
        migrations.CreateModel(
            name='Educacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango', models.IntegerField(choices=[(1, 'Hombres mayores 31 a\xf1os'), (2, 'Mujeres mayores 31 a\xf1os'), (3, 'Hombre joven 19 a 30 a\xf1os'), (4, 'Mujer joven 19 a 30 a\xf1os'), (5, 'Hombre adoles. 13 a 18 a\xf1os'), (6, 'Mujer adoles. 13 a 18 a\xf1os'), (7, 'Ni\xf1os 5 a 12 a\xf1os'), (8, 'Ni\xf1as 5 a 12 a\xf1os'), (9, 'Ancianos (> 64 a\xf1os)'), (10, 'Ancianas (> 64 a\xf1os)')], verbose_name='Selecci\xf3n')),
                ('numero_total', models.IntegerField(verbose_name='N\xfamero total')),
                ('no_lee_ni_escribe', models.IntegerField(verbose_name='No lee, ni escribe')),
                ('primaria_incompleta', models.IntegerField(verbose_name='Primaria incompleta')),
                ('primaria_completa', models.IntegerField(verbose_name='Primaria completa')),
                ('secundaria_incompleta', models.IntegerField(verbose_name='Secundaria incompleta')),
                ('bachiller', models.IntegerField(verbose_name='Bachiller')),
                ('universitario_tecnico', models.IntegerField(verbose_name='Universitario o t\xe9cnico')),
                ('viven_fuera', models.IntegerField(verbose_name='N\xfamero de personas que viven fuera de la finca')),
            ],
            options={
                'verbose_name': '1-2 Nivel de escolaridad de los miembros de la familia',
                'verbose_name_plural': '1-2 Nivel de escolaridad de los miembros de la familia',
            },
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha de la encuesta')),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Encuestadores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.Organizacion')),
            ],
            options={
                'verbose_name': 'Encuestador',
                'verbose_name_plural': 'Encuestadores',
            },
        ),
        migrations.CreateModel(
            name='Entrevistados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre del jefe de familia')),
                ('cedula', models.CharField(max_length=20, verbose_name='N\xfamero de Cedula')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('comunidad', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='municipio', chained_model_field='municipio', on_delete=django.db.models.deletion.CASCADE, to='lugar.Comunidad')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.Departamento')),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='departamento', chained_model_field='departamento', on_delete=django.db.models.deletion.CASCADE, to='lugar.Municipio')),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.Organizacion', verbose_name='A que Organizaci\xf3n pertenece')),
            ],
            options={
                'verbose_name': 'Informaci\xf3n del Entrevistado',
                'verbose_name_plural': 'Informaci\xf3n del Entrevistado',
            },
        ),
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miembros', models.IntegerField(verbose_name='N\xfamero de miembros')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta')),
            ],
            options={
                'verbose_name': '1-1 Miembros de la Familia',
                'verbose_name_plural': '1-1 Miembros de la Familia',
            },
        ),
        migrations.CreateModel(
            name='Profesiones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Profesi\xf3n',
                'verbose_name_plural': 'Profesiones',
            },
        ),
        migrations.CreateModel(
            name='SituacionesPropiedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Situaci\xf3n de la Propiedad',
                'verbose_name_plural': 'Situaciones de las Propiedades',
            },
        ),
        migrations.CreateModel(
            name='TenenciaPropiedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dueno_propiedad', models.IntegerField(choices=[(1, 'Si'), (2, 'No')], verbose_name='Son ustedes due\xf1os de la propiedad')),
                ('si', models.IntegerField(blank=True, choices=[(1, 'A nombre del Hombre'), (2, 'A nombre de la Mujer'), (3, 'A nombre de Hijas/hijos'), (4, 'A nombre del Hombre y Mujer'), (5, 'Colectivo')], null=True, verbose_name='En el caso Si, a nombre de quien esta la propiedad')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta')),
                ('no', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='productores.SituacionesPropiedad', verbose_name='En el caso que diga NO, especifique situaci\xf3n en que esta la propiedad')),
            ],
            options={
                'verbose_name': '2 Tenencia de Propiedad',
                'verbose_name_plural': '2 Tenencia de Propiedad',
            },
        ),
        migrations.AddField(
            model_name='entrevistados',
            name='profesion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Profesiones', verbose_name='Profesi\xf3n u oficio'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='encuestador',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='organizacion', chained_model_field='organizacion', on_delete=django.db.models.deletion.CASCADE, to='productores.Encuestadores', verbose_name='Nombre del Encuestador'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='entrevistado',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='organizacion', chained_model_field='organizacion', on_delete=django.db.models.deletion.CASCADE, to='productores.Entrevistados', verbose_name='Nombre del jefe de familia'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='organizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.Organizacion', verbose_name='Nombre de la Organizaci\xf3n'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='educacion',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta'),
        ),
        migrations.AddField(
            model_name='detalleareafinca',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta'),
        ),
        migrations.AddField(
            model_name='areafinca',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta'),
        ),
    ]