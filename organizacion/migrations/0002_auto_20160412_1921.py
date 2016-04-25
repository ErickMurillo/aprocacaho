# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 19:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AspectosJuridicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiene_p_juridica', models.IntegerField(choices=[(1, 'Si'), (2, 'No')], verbose_name='Personer\xeda jur\xeddica')),
                ('act_p_juridica', models.IntegerField(choices=[(1, 'Si'), (2, 'No')], verbose_name='Actualizaci\xf3n personer\xeda jur\xeddica')),
                ('solvencia_tributaria', models.IntegerField(choices=[(1, 'Si'), (2, 'No')], verbose_name='Cuenta con Registro Tributario Nacional Num\xe9rico')),
                ('junta_directiva', models.IntegerField(choices=[(1, 'Si'), (2, 'No')], verbose_name='Junta Directiva certificada')),
                ('mujeres', models.IntegerField(verbose_name='Miembros mujeres JD')),
                ('hombres', models.IntegerField(verbose_name='Miembros hombres JD')),
                ('lista_socios', models.IntegerField(choices=[(1, 'Si'), (2, 'No')], verbose_name='Lista socias/os esta actualizada y certificada')),
                ('ursac', models.CharField(blank=True, max_length=50, null=True, verbose_name='N\xfamero de la Unidad de Registro y Seguimiento de las Asociaciones Civiles (URSAC)')),
            ],
            options={
                'verbose_name_plural': 'II. Aspectos jur\xeddicos',
            },
        ),
        migrations.CreateModel(
            name='CertificacionOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corriente', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Org\xe1nico'), (2, 'Comercio Justo'), (3, 'UTZ')], max_length=5)),
                ('fermentado', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Org\xe1nico'), (2, 'Comercio Justo'), (3, 'UTZ')], max_length=5)),
            ],
            options={
                'verbose_name_plural': 'Tipo de certificaci\xf3n',
            },
        ),
        migrations.CreateModel(
            name='Comercializacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seleccion', models.IntegerField(choices=[(1, 'No. de socios que entregaron cacao al acopio'), (2, 'No. de No socios que entregaron cacao al acopio'), (3, 'Cantidad de cacao en baba acopiado por la organizaci\xf3n'), (4, 'Cantidad de cacao seco comercializado por la organizaci\xf3n')])),
                ('corriente', models.FloatField()),
                ('fermentado', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'VI. Informaci\xf3n sobre la Comercializaci\xf3n',
            },
        ),
        migrations.CreateModel(
            name='DatosProductivos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productores_socios', models.IntegerField()),
                ('productoras_socias', models.IntegerField()),
                ('productores_no_socios', models.IntegerField()),
                ('productoras_no_socias', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'IV- Informaci\xf3n sobre datos productivos',
            },
        ),
        migrations.CreateModel(
            name='DatosProductivosTabla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.IntegerField(choices=[(1, '\xc1rea total Establecida (Mz)'), (2, '\xc1rea certificadas (Mz)'), (3, '\xc1rea convencional (Mz)'), (4, 'Rendimiento promedio de cacao en baba por Mz'), (5, 'Rendimiento promedio de cacao seco por Mz')])),
                ('productores_socios', models.FloatField()),
                ('productores_no_socios', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'IV- Informaci\xf3n sobre datos productivos',
            },
        ),
        migrations.CreateModel(
            name='DestinoProdCorriente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destino', models.IntegerField(choices=[(1, 'Intermediario local'), (2, 'APROCACAHO'), (3, 'Chocolats Halba'), (4, 'Otros')])),
                ('entrega', models.FloatField(verbose_name='% de entrega')),
            ],
            options={
                'verbose_name_plural': 'Destino de la producci\xf3n Cacao corriente',
            },
        ),
        migrations.CreateModel(
            name='DestinoProdFermentado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destino', models.IntegerField(choices=[(1, 'Intermediario local'), (2, 'APROCACAHO'), (3, 'Chocolats Halba'), (4, 'Otros')])),
                ('entrega', models.FloatField(verbose_name='% de entrega')),
            ],
            options={
                'verbose_name_plural': 'Destino de la producci\xf3n Cacao fermentado',
            },
        ),
        migrations.CreateModel(
            name='Documentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentos', models.IntegerField(choices=[(1, 'Poseen estatutos'), (2, 'Poseen libro de Actas'), (3, 'Cuenta con un Reglamento Interno'), (4, 'Cuenta con un Plan Estrat\xe9gico'), (5, 'Cuenta con un Plan Opeativo Anual'), (6, 'Cuenta con un Plan de Negocios'), (7, 'Cuentan con Plan de Acopio')])),
                ('si_no', models.IntegerField(choices=[(1, 'Si'), (2, 'No')], verbose_name='Si/No')),
                ('fecha', models.DateField(verbose_name='Fecha de elaboraci\xf3n u actualizaci\xf3n')),
            ],
            options={
                'verbose_name_plural': 'III. Informaci\xf3n sobre documentaci\xf3n',
            },
        ),
        migrations.CreateModel(
            name='EncuestaOrganicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('anno', models.IntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Encuesta',
                'verbose_name_plural': 'Encuestas',
            },
        ),
        migrations.CreateModel(
            name='Financiamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seleccion', models.IntegerField(choices=[(1, 'La propia organizaci\xf3n'), (2, 'Cooperaci\xf3n Internacional'), (3, 'Cr\xe9dito bancario'), (4, 'Financiamiento del comprador')], verbose_name='\xbfQui\xe9n financia la producci\xf3n?')),
                ('monto', models.FloatField(verbose_name='Monto de financiamiento (Lp)')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion')),
            ],
            options={
                'verbose_name_plural': 'VII. Informaci\xf3n sobre financiamiento',
            },
        ),
        migrations.CreateModel(
            name='FinanciamientoProductores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financiamiento', models.IntegerField(choices=[(1, 'Si'), (2, 'No')])),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion')),
            ],
            options={
                'verbose_name_plural': 'Financiamiento a productores',
            },
        ),
        migrations.CreateModel(
            name='Infraestructura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(1, 'Centro de Acopio central'), (2, 'Centro de acopio comunitario'), (3, 'Secadoras artificiales'), (4, 'Planta de procesamiento'), (5, 'Bodegas'), (6, 'Cuartos fr\xedos'), (7, 'Oficina'), (8, 'Medios de Transporte'), (9, '\xc1rea de fermentado'), (10, 'Secadoras solares'), (11, 'Viveros')], verbose_name='Tipo de Infraestructura')),
                ('cantidad', models.IntegerField()),
                ('capacidad', models.FloatField(verbose_name='Capacidad (qq)')),
                ('anno_construccion', models.DateField(verbose_name='A\xf1o de construcci\xf3n')),
                ('estado', models.IntegerField(choices=[(1, 'Bueno'), (2, 'Malo'), (3, 'Regular')], verbose_name='Estado de infraestructura')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion')),
            ],
            options={
                'verbose_name_plural': 'V. Informaci\xf3n sobre instalaciones y equipos',
            },
        ),
        migrations.CreateModel(
            name='ListaMiembros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre y apellido')),
                ('cargo', models.CharField(max_length=100)),
                ('telefonos', models.CharField(max_length=100)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion')),
            ],
            options={
                'verbose_name_plural': 'Lista de miembros de la junta directiva',
            },
        ),
        migrations.CreateModel(
            name='NivelCumplimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentos', models.IntegerField(choices=[(1, 'Poseen estatutos'), (2, 'Poseen libro de Actas'), (3, 'Cuenta con un Reglamento Interno'), (4, 'Cuenta con un Plan Estrat\xe9gico'), (5, 'Cuenta con un Plan Opeativo Anual'), (6, 'Cuenta con un Plan de Negocios'), (7, 'Cuentan con Plan de Acopio')])),
                ('cumplimiento', models.IntegerField(choices=[(1, '10-30%'), (2, '31-60%'), (3, '61-100%')])),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion')),
            ],
            options={
                'verbose_name_plural': 'Nivel de cumplimiento',
            },
        ),
        migrations.CreateModel(
            name='RespuestaSi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.FloatField()),
                ('cantidad_manzanas', models.FloatField()),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion')),
            ],
            options={
                'verbose_name_plural': 'En el caso que responda \u201cSI\u201d',
            },
        ),
        migrations.AlterField(
            model_name='organizacion',
            name='direccion',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Direcci\xf3n fisica de la Organizaci\xf3n'),
        ),
        migrations.AddField(
            model_name='encuestaorganicacion',
            name='organizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Organizacion', to='organizacion.Organizacion'),
        ),
        migrations.AddField(
            model_name='encuestaorganicacion',
            name='usuario',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentacion',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
        migrations.AddField(
            model_name='destinoprodfermentado',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
        migrations.AddField(
            model_name='destinoprodcorriente',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
        migrations.AddField(
            model_name='datosproductivostabla',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
        migrations.AddField(
            model_name='datosproductivos',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
        migrations.AddField(
            model_name='comercializacion',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
        migrations.AddField(
            model_name='certificacionorg',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
        migrations.AddField(
            model_name='aspectosjuridicos',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizacion.EncuestaOrganicacion'),
        ),
    ]