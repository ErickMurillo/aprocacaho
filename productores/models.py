# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizacion.models import *
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField

# Create your models here.
class Profesiones(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Profesión"
		verbose_name_plural = "Profesiones"

class SituacionesPropiedad(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Situación de la Propiedad"
		verbose_name_plural = "Situaciones de las Propiedades"

class Tipos_Servicio(models.Model):
	servicio = models.CharField(max_length=200)

	def __unicode__(self):
		return self.servicio

	class Meta:
		verbose_name = "Tipo de Servicio que recibe"
		verbose_name_plural = "Tipos de Servicios que recibe"

class Beneficios(models.Model):
	beneficio = models.CharField(max_length=200)

	def __unicode__(self):
		return self.beneficio

	class Meta:
		verbose_name = "Beneficio de estar asociado"
		verbose_name_plural = "Beneficios de estar asociado"
		
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
		(10,'Ancianas (> 64 años)'),
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

PROPIEDAD_CHOICE = (
	(1,'A nombre del Hombre'),
	(2,'A nombre de la Mujer'),
	(3,'A nombre de Hijas/hijos'),
	(4,'A nombre del Hombre y Mujer'),
	(5,'Colectivo'),
	)

SI_NO_CHOICES = (
	(1,'Si'),
	(2,'No')
	)

class TenenciaPropiedad(models.Model):
	dueno_propiedad = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Son ustedes dueños de la propiedad')
	si = models.IntegerField(choices=PROPIEDAD_CHOICE,
		verbose_name='En el caso Si, a nombre de quien esta la propiedad',null=True,blank=True)
	no = models.ForeignKey(SituacionesPropiedad,verbose_name='En el caso que diga NO, especifique situación en que esta la propiedad',
		null=True,blank=True)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "2 Tenencia de Propiedad"
		verbose_name_plural = "2 Tenencia de Propiedad"

class AreaFinca(models.Model):
	area = models.FloatField(verbose_name='3.1 Área total en manzanas que tiene la propiedad')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "3 Uso de la Tierra"
		verbose_name_plural = "3 Uso de la Tierra"

CHOICE_TIERRA = (
    (1,'Bosque'),
    (2,'Tacotal o regeneración natural'),
    (3,'Cultivo anual ( que produce en el año)'),
    (4,'Plantación forestal ( madera y leña)'),
    (5,'Área de pastos abierto'),
    (6,'Área de pastos con árboles'),
    (7,'Cultivo perenne (frutales)'),
    (8,'Cultivo semi-perenne (musácea, piña)'),
    (9,'Solo destinado para cacao'),
    (10,'Huerto mixto con cacao'),
    (11,'Otros'),
    )

class DetalleAreaFinca(models.Model):
	seleccion = models.IntegerField(choices=CHOICE_TIERRA,verbose_name='3.2 Distribución de la finca')
	area = models.FloatField(verbose_name='Área en Mz')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "3 Uso de la Tierra"
		verbose_name_plural = "3 Uso de la Tierra"

REFORESTACION_CHOICE = (
	(1,'Enriquecimiento de los bosques'),
    (2,'Protección de fuentes de agua'),
    (3,'Establecimiento de cercas viva'),
    (4,'Establecimiento de viveros'),
    (5,'Siembra de árboles en cacao'),
    (6,'Plantaciones forestales'),
    (7,'Siembra de árboles en potrero'),
    (8,'Parcelas frutales'),
	)

class Reforestacion(models.Model):
	seleccion = models.IntegerField(choices=REFORESTACION_CHOICE)
	respuesta = models.IntegerField(choices=SI_NO_CHOICES)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "4 Reforestación"
		verbose_name_plural = "4 Reforestación"

TEXTURA_CHOICES = (
	(1,'Arcilloso'),
	(2,'Limoso'),
	(3,'Arenoso'),
	(4,'Franco'),
	)

PENDIENTE_CHOICES = (
	(1,'Plana (0-10%)'),
	(2,'Inclinada (11-30%)'),
	(3,'Muy inclinada (> 30%)'),
	)

HOJARASCA_CHOICES = (
	(1,'Alta'),
	(2,'Medio'),
	(3,'Baja'),
	)

PROFUNDIDAD_CHOICES = (
	(1,'Poco profundo (< 50 cm)'),
	(2,'Medio profundo (51-80 cm)'),
	(3,'Muy profundo (> 80 cm)'),
	)

DRENAJE_CHOICES = (
	(1,'Bueno (no se encharca)'),
	(2,'Regular (poco se encharca)'),
	(3,'Malo (se encharca con lluvia)'),
	)

class CaracterizacionTerreno(models.Model):
	textura_suelo = models.IntegerField(choices=TEXTURA_CHOICES,verbose_name='¿Cuál es el tipo de textura del suelo?')
	pendiente_terreno = models.IntegerField(choices=PENDIENTE_CHOICES,verbose_name='¿Cuál es la pendiente del terreno?')
	contenido_hojarasca = models.IntegerField(choices=HOJARASCA_CHOICES,verbose_name='¿Cómo en el contenido de hojarasca?')
	porfundidad_suelo = models.IntegerField(choices=PROFUNDIDAD_CHOICES,verbose_name='¿Cuál es la profundidad de suelo?')
	drenaje_suelo = models.IntegerField(choices=DRENAJE_CHOICES,verbose_name='¿Cómo en el drenaje del suelo?')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "5 Caracterización de terreno"
		verbose_name_plural = "5 Caracterización de terreno"

RIESGOS_CHOICES = (
	(1,'Fuerte'),
	(2,'Poco fuerte'),
	(3,'Leve'),
	(4,'No hubo'),
	)

class FenomenosNaturales(models.Model):
	sequia = models.IntegerField(choices=RIESGOS_CHOICES,verbose_name='Sequía')
	innundacion = models.IntegerField(choices=RIESGOS_CHOICES,verbose_name='Inundación')
	lluvia = models.IntegerField(choices=RIESGOS_CHOICES)
	viento = models.IntegerField(choices=RIESGOS_CHOICES)
	deslizamiento = models.IntegerField(choices=RIESGOS_CHOICES)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 Fenómenos naturales"
		verbose_name_plural = "6 Fenómenos naturales"

P_IMPRODUCTIVAS_CHOICES = (
	(1,'Alto (40%)'),
	(2,'Medio (30%)'),
	(3,'Baja (10%)'),
	)

class RazonesAgricolas(models.Model):
	plantas_improductivas = models.IntegerField(choices=P_IMPRODUCTIVAS_CHOICES)
	plagas_enfermedades = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Plagas y enfermedades')
	quemas = models.IntegerField(choices=SI_NO_CHOICES)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 Razones agrícolas"
		verbose_name_plural = "6 Razones agrícolas"

class RazonesMercado(models.Model):
	bajo_precio = models.IntegerField(choices=SI_NO_CHOICES)
	falta_venta = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Falta de venta')
	estafa_contrato = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Estafa de contrato')
	calidad_producto = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Mala calidad de producto')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 Razones de mercado"
		verbose_name_plural = "6 Razones de mercado"

class Inversion(models.Model):
	invierte_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Invierte en cacao')
	interes_invertrir = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Interés de invertir')
	falta_credito = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Falta de crédito')
	altos_intereses = models.IntegerField(choices=SI_NO_CHOICES)
	robo_producto = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Robo de producto')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 Inversión"
		verbose_name_plural = "6 Inversión"

VENTA_CHOICES = (
	(1,'Individual'),
	(2,'A través de la Cooperativa'),
	)

TECNOLOGIA_CHOICES = (
	(1,'Propia'),
	(2,'Cooperativa'),
	)

class MitigacionRiesgos(models.Model):
	monitoreo_plagas = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Realiza monitoreo de plagas y enfermedades?')
	manejo_cultivo = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Cuenta con un manejo adecuado para el cultivo?')
	manejo_recursos = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Disponen suficiente recursos para manejo de finca?')
	almacenamiento_agua = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Cuenta con obras para almacenamiento de agua?')
	distribucion_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Participan en cadena de distribución de producto cacao?')
	venta_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Cuenta con un contrato para la venta de cacao?')
	si_venta_cacao = models.IntegerField(choices=VENTA_CHOICES,verbose_name='Si responde Si: favor indicar si el contrato lo hace')
	tecnologia_secado = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Dispone de tecnología para el secado y almacenamiento de cosecha?')
	si_tecnologia_secado = models.IntegerField(choices=TECNOLOGIA_CHOICES,verbose_name='Si responde Si: favor indicar si la tecnología de secado y almacenamiento es')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "7 Mitigación de los riesgos"
		verbose_name_plural = "7 Mitigación de los riesgos"

class OrganizacionAsociada(models.Model):
	socio = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Trabaja con alguna Organización/Institución')
	organizacion = models.ManyToManyField(Organizacion,verbose_name='Organización/Institución con la que trabaja',blank=True)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "8 Org. productiva-comercial asociado"
		verbose_name_plural = "8 Org. productiva-comercial asociado"

class ServiciosOrganizado(models.Model):
	tipos_servicio = models.ManyToManyField(Tipos_Servicio,verbose_name='Tipos de servicios que recibe')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "8 Org. productiva-comercial asociado"
		verbose_name_plural = "8 Org. productiva-comercial asociado"

class BeneficiosOrganizado(models.Model):
	beneficios = models.ManyToManyField(Beneficios,verbose_name='Beneficios de estar asociado')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "8 Org. productiva-comercial asociado"
		verbose_name_plural = "8 Org. productiva-comercial asociado"

class AreaCacao(models.Model):
	area = models.FloatField(verbose_name='Área total de cacao establecida en finca(Mz)')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "9 Área de cacao en finca"
		verbose_name_plural = "9 Área de cacao en fincas"

EDAD_PLANTA_CHOICES = (
	(1,'Menor de un año'),
	(2,'De 1 a 3 años'),
	(3,'De 4 a 10 años'),
	(4,'De 10 a 20 años'),
	(5,'Mayores de 20 años'),
	)

class Plantacion(models.Model):
	edad = models.IntegerField(choices=EDAD_PLANTA_CHOICES)
	area = models.FloatField(verbose_name='Área en Mz')
	edad_real = models.FloatField(verbose_name='Edad real de la Plantación (años)')
	numero_plantas = models.IntegerField(verbose_name='Número de plantas en el área')
	plantas_semilla = models.IntegerField(verbose_name='Número de plantas establecidas por semilla')
	plantas_injerto = models.IntegerField(verbose_name='Número de plantas establecidas por injerto')
	plantas_improductivas = models.IntegerField(verbose_name='Número de plantas improductivas en el área')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "9-1 Edad de la plantación"
		verbose_name_plural = "9-1 Edad de la plantación"

MESES_CHOICES = (
	(1,'Enero'),
	(2,'Febrero'),
	(3,'Marzo'),
	(4,'Abril'),
	(5,'Mayo'),
	(6,'Junio'),
	(7,'Julio'),
	(8,'Agosto'),
	(9,'Septiembre'),
	(10,'Octubre'),
	(11,'Noviembre'),
	(12,'Diciembre'),
	)

class ProduccionCacao(models.Model):
	cacao_baba = models.FloatField(verbose_name='Producción cacao en baba (qq baba/fresco)')
	meses = MultiSelectField(choices=MESES_CHOICES,verbose_name='Meses de mayor producción de cacao')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "9-2 Producción de cacao último año"
		verbose_name_plural = "9-2 Producción de cacao último año"