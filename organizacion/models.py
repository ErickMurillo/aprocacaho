# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from lugar.models import *
from sorl.thumbnail import ImageField
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField

# Create your models here.
STATUS_CHOICES = (
	(1,'ONG'),
	(2, 'Cooperativa'),
	(3, 'Unión de Cooperativa'),
	)

class Organizacion(models.Model):
	nombre = models.CharField(max_length=200,verbose_name='Nombre de la Organización')
	siglas = models.CharField(max_length=200)
	fundacion = models.DateField(verbose_name='Año de fundación',null=True,blank=True)
	gerente = models.CharField(max_length=200,verbose_name='Presidente/Administrador',null=True,blank=True)
	status = models.IntegerField(verbose_name='Estatus Legal',choices=STATUS_CHOICES)
	direccion = models.CharField(max_length=300,null=True,blank=True,verbose_name='Dirección fisica de la Organización')
	departamento = models.ForeignKey(Departamento)
	municipio = ChainedForeignKey(
                                Municipio,
                                chained_field="departamento",
                                chained_model_field="departamento",
                                show_all=False, auto_choose=True)
	telefono = models.IntegerField(verbose_name='Número telefónico',null=True,blank=True)
	email = models.EmailField(null=True,blank=True)
	web = models.URLField(verbose_name='Sitio web',null=True,blank=True)
	contacto = models.CharField(max_length=200,verbose_name='Persona de contacto',null=True,blank=True)
	logo = ImageField(upload_to='logo/',null=True,blank=True)
	slug = models.SlugField(editable=False, max_length=450)

	def __unicode__(self):
		return self.siglas

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.siglas)
		super(Organizacion, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Organización"
		verbose_name_plural = "Organizaciones"

class EncuestaOrganicacion(models.Model):
		fecha = models.DateField()
		organizacion = models.ForeignKey(Organizacion,related_name='Organizacion')
		anno = models.IntegerField(editable=False)
		usuario = models.ForeignKey(User,related_name='User',editable=False)

		def __unicode__(self):
			return self.organizacion.siglas

		def save(self, *args, **kwargs):
			self.anno = self.fecha.year
			super(Encuesta_Org, self).save(*args, **kwargs)

		class Meta:
			verbose_name = "Encuesta"
			verbose_name_plural = "Encuestas"

SI_NO_CHOICES = (
	(1,'Si'),
	(2,'No'),
	)

class AspectosJuridicos(models.Model):
	tiene_p_juridica = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Personería jurídica')
	act_p_juridica = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Actualización personería jurídica')
	solvencia_tributaria = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Cuenta con Registro Tributario Nacional Numérico')
	junta_directiva = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Junta Directiva certificada')
	mujeres = models.IntegerField(verbose_name='Miembros mujeres JD')
	hombres = models.IntegerField(verbose_name='Miembros hombres JD')
	lista_socios = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Lista socias/os esta actualizada y certificada')
	ursac = models.CharField(max_length=50,verbose_name='Número de la Unidad de Registro y Seguimiento de las Asociaciones Civiles (URSAC)',null=True,blank=True)
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "II. Aspectos jurídicos"

class ListaMiembros(models.Model):
	nombre = models.CharField(max_length=100,verbose_name='Nombre y apellido')
	cargo = models.CharField(max_length=100)
	telefonos = models.CharField(max_length=100)
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "Lista de miembros de la junta directiva"

DOCUMENTOS_CHOICES = (
	(1,'Poseen estatutos'),
	(2,'Poseen libro de Actas'),
	(3,'Cuenta con un Reglamento Interno'),
	(4,'Cuenta con un Plan Estratégico'),
	(5,'Cuenta con un Plan Opeativo Anual'),
	(6,'Cuenta con un Plan de Negocios'),
	(7,'Cuentan con Plan de Acopio'),
	)

class Documentacion(models.Model):
	documentos = models.IntegerField(choices=DOCUMENTOS_CHOICES)
	si_no = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Si/No')
	fecha = models.DateField(verbose_name='Fecha de elaboración u actualización')
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "III. Información sobre documentación"

CUMPLIMIENTO_CHOICES = (
	(1,'10-30%'),
	(2,'31-60%'),
	(3,'61-100%')
)

class NivelCumplimiento(models.Model):
	documentos = models.IntegerField(choices=DOCUMENTOS_CHOICES)
	cumplimiento = models.IntegerField(choices=CUMPLIMIENTO_CHOICES)
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "Nivel de cumplimiento"

class DatosProductivos(models.Model):
	productores_socios = models.IntegerField()
	productoras_socias = models.IntegerField()
	productores_no_socios = models.IntegerField()
	productoras_no_socias = models.IntegerField()
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = 'IV- Información sobre datos productivos'

DATOS_CHOICES = (
	(1,'Área total Establecida (Mz)'),
	(2,'Área certificadas (Mz)'),
	(3,'Área convencional (Mz)'),
	(4,'Rendimiento promedio de cacao en baba por Mz'),
	(5,'Rendimiento promedio de cacao seco por Mz'),
)

class DatosProductivosTabla(models.Model):
	pregunta = models.IntegerField(choices=DATOS_CHOICES)
	productores_socios = models.FloatField()
	productores_no_socios = models.FloatField()
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = 'IV- Información sobre datos productivos'

INFRAESTRUCTURA_CHOICES = (
	(1,'Centro de Acopio central'),
	(2,'Centro de acopio comunitario'),
	(3,'Secadoras artificiales'),
	(4,'Planta de procesamiento'),
	(5,'Bodegas'),
	(6,'Cuartos fríos'),
	(7,'Oficina'),
	(8,'Medios de Transporte'),
	(9,'Área de fermentado'),
	(10,'Secadoras solares'),
	(11,'Viveros'),
	)

ESTADO_CHOICES = (
	(1,'Bueno'),
	(2,'Malo'),
	(3,'Regular'),
	)

class Infraestructura(models.Model):
	tipo = models.IntegerField(choices=INFRAESTRUCTURA_CHOICES,verbose_name='Tipo de Infraestructura')
	cantidad = models.IntegerField()
	capacidad = models.FloatField(verbose_name='Capacidad (qq)')
	anno_construccion = models.DateField(verbose_name='Año de construcción')
	estado = models.IntegerField(choices=ESTADO_CHOICES,verbose_name='Estado de infraestructura')
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "V. Información sobre instalaciones y equipos"

COMERCIO_CHOICES = (
	(1,'No. de socios que entregaron cacao al acopio'),
	(2,'No. de No socios que entregaron cacao al acopio'),
	(3,'Cantidad de cacao en baba acopiado por la organización'),
	(4,'Cantidad de cacao seco comercializado por la organización'),
)

class Comercializacion(models.Model):
	seleccion = models.IntegerField(choices=COMERCIO_CHOICES)
	corriente = models.FloatField()
	fermentado = models.FloatField()
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "VI. Información sobre la Comercialización"

CERTIFICACION_CHOICES = (
	(1,'Orgánico'),
	(2,'Comercio Justo'),
	(3,'UTZ'),
)

class CertificacionOrg(models.Model):
	corriente = MultiSelectField(choices=CERTIFICACION_CHOICES)
	fermentado = MultiSelectField(choices=CERTIFICACION_CHOICES)
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "Tipo de certificación"

DESTINO_CHOICES = (
	(1,'Intermediario local'),
	(2,'APROCACAHO'),
	(3,'Chocolats Halba'),
	(4,'Otros'),
)

class DestinoProdCorriente(models.Model):
	destino = models.IntegerField(choices=DESTINO_CHOICES)
	entrega = models.FloatField(verbose_name='% de entrega')
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "Destino de la producción Cacao corriente"

class DestinoProdFermentado(models.Model):
	destino = models.IntegerField(choices=DESTINO_CHOICES)
	entrega = models.FloatField(verbose_name='% de entrega')
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "Destino de la producción Cacao fermentado"

FINANACIA_CHOICES = (
	(1,'La propia organización'),
	(2,'Cooperación Internacional'),
	(3,'Crédito bancario'),
	(4,'Financiamiento del comprador'),
)

class Financiamiento(models.Model):
	seleccion = models.IntegerField(choices=FINANACIA_CHOICES,verbose_name='¿Quién financia la producción?')
	monto = models.FloatField(verbose_name='Monto de financiamiento (Lp)')
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "VII. Información sobre financiamiento"

class FinanciamientoProductores(models.Model):
	financiamiento = models.IntegerField(choices=SI_NO_CHOICES)
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "Financiamiento a productores"

class RespuestaSi(models.Model):
	monto = models.FloatField()
	cantidad_manzanas = models.FloatField()
	encuesta = models.ForeignKey(EncuestaOrganicacion)

	class Meta:
		verbose_name_plural = "En el caso que responda “SI”"
