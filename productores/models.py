# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizacion.models import *
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
class Profesiones(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Profesión"
		verbose_name_plural = "Profesiones"
		
class Entrevistados(models.Model):
	nombre =  models.CharField(max_length=200,verbose_name='Nombre del jefe de familia')
	cedula = models.CharField(max_length=20,verbose_name='Número de Cedula')
	fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
	profesion = models.ForeignKey(Profesiones,verbose_name='Profesión u oficio')
	organizacion = models.ForeignKey(Organizacion,verbose_name='A que Organización pertenece')
	departamento = models.ForeignKey(Departamento)
	municipio = ChainedForeignKey(
                                Municipio,
                                chained_field="departamento",
                                chained_model_field="departamento",
                                show_all=False, auto_choose=True)
	comunidad = ChainedForeignKey(
                                Comunidad,
                                chained_field="municipio",
                                chained_model_field="municipio",
                                show_all=False, auto_choose=True)
	latitud = models.FloatField(null=True,blank=True)
	longitud = models.FloatField(null=True,blank=True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Información del Entrevistado"
		verbose_name_plural = "Información del Entrevistado"

class Encuestadores(models.Model):
	nombre = models.CharField(max_length=200)
	organizacion = models.ForeignKey(Organizacion)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Encuestador"
		verbose_name_plural = "Encuestadores"

class Encuesta(models.Model):
	fecha = models.DateField(verbose_name='Fecha de la encuesta')
	organizacion = models.ForeignKey(Organizacion,verbose_name='Nombre de la Organización')
	encuestador = ChainedForeignKey(
                                Encuestadores,
                                chained_field="organizacion",
                                chained_model_field="organizacion",
                                show_all=False, auto_choose=True,
                                verbose_name='Nombre del Encuestador')
	entrevistado =  ChainedForeignKey(
                                Entrevistados,
                                chained_field="organizacion",
                                chained_model_field="organizacion",
                                show_all=False, auto_choose=True,
                                verbose_name='Nombre del jefe de familia')
                                
	year = models.IntegerField()
	usuario = models.ForeignKey(User)


	def __unicode__(self):
		return self.entrevistado.nombre

	def save(self, *args, **kwargs):
		self.year = self.fecha.year
		super(Encuesta, self).save(*args, **kwargs)

class Familia(models.Model):
	miembros = models.IntegerField(verbose_name='Número de miembros')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "1-1 Miembros de la Familia"
		verbose_name_plural = "1-1 Miembros de la Familia"

RANGOS_CHOICE = (
		(1,'Hombres mayores 31 años'),
		(2,'Mujeres mayores 31 años'),
		(3,'Hombre joven 19 a 30 años'),
		(4,'Mujer joven 19 a 30 años'),
		(5,'Hombre adoles. 13 a 18 años'),
		(6,'Mujer adoles. 13 a 18 años'),
		(7,'Niños 5 a 12 años'),
		(8,'Niñas 5 a 12 años'),
		(9,'Ancianos (> 64 años)'),
		(9,'Ancianas (> 64 años)'),
		)

class Educacion(models.Model):
	rango = models.IntegerField(choices=RANGOS_CHOICE,verbose_name='Selección')
	numero_total = models.IntegerField(verbose_name='Número total')
	no_lee_ni_escribe = models.IntegerField(verbose_name='No lee, ni escribe')
	primaria_incompleta = models.IntegerField(verbose_name='Primaria incompleta')
	primaria_completa = models.IntegerField(verbose_name='Primaria completa')
	secundaria_incompleta = models.IntegerField(verbose_name='Secundaria incompleta')
	bachiller = models.IntegerField(verbose_name='Bachiller')
	universitario_tecnico = models.IntegerField(verbose_name='Universitario o técnico')
	viven_fuera = models.IntegerField(verbose_name='Número de personas que viven fuera de la finca')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "1-2 Nivel de escolaridad de los miembros de la familia"
		verbose_name_plural = "1-2 Nivel de escolaridad de los miembros de la familia"