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

class TiposServicio(models.Model):
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

class QuienCertifica(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Quién certifica"
		verbose_name_plural = "Quienes certifican"

class ActividadesProduccion(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Actividad de Producción"
		verbose_name_plural = "Actividades de Producción"

class DestinoIngresos(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Destino de ingresos percibidos"
		verbose_name_plural = "Destino de ingresos percibidos"

class OtrosIngresos(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Otra fuente de ingreso en la finca"
		verbose_name_plural = "Otras fuentes de ingreso en la finca"

class ProblemasArea1(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Problemas en áreas de 1 a 3 años"
		verbose_name_plural = "Problemas en áreas de 1 a 3 años"

class ProblemasArea2(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Problemas en áreas de 4 a 10 años"
		verbose_name_plural = "Problemas en áreas de 4 a 10 años"

class ProblemasArea3(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Problemas en áreas de 10 a 20 años"
		verbose_name_plural = "Problemas en áreas de 10 a 20 años"

CHOICE_SEXO = (
    (1, 'Mujer'),
    (2, 'Hombre'),
  )

class Entrevistados(models.Model):
	nombre =  models.CharField(max_length=200,verbose_name='Nombre del jefe de familia')
	cedula = models.CharField(max_length=20,verbose_name='Número de Cedula')
	fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
	sexo = models.IntegerField(choices=CHOICE_SEXO)
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
		verbose_name = "1.1 Miembros de la Familia"
		verbose_name_plural = "1.1 Miembros de la Familia"

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
		verbose_name = "1.2 Nivel de escolaridad de los miembros de la familia"
		verbose_name_plural = "1.2 Nivel de escolaridad de los miembros de la familia"

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
	area = models.FloatField(verbose_name='Área total en manzanas que tiene la propiedad')
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
	tipos_servicio = models.ManyToManyField(TiposServicio,verbose_name='Tipos de servicios que recibe')
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
		verbose_name = "9.1 Edad de la plantación"
		verbose_name_plural = "9.1 Edad de la plantación"

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
		verbose_name = "9.2 Producción de cacao último año"
		verbose_name_plural = "9.2 Producción de cacao último año"

CERTIFICACIONES_CHOICES = (
	(1,'Convencional'),
	(2,'Orgánico'),
	(3,'UTZ/Sello'),
	(4,'FAIR TRADE'),
	)

PAGA_CERT_CHOICES = (
	(1,'Productor'),
	(2,'Cooperativa'),
	)

class Certificacion(models.Model):
	cacao_certificado = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Sus área de cacao están certificadas')
	tipo = MultiSelectField(choices=CERTIFICACIONES_CHOICES,verbose_name='Tipo de certificación',blank=True,null=True)
	quien_certifica = models.ManyToManyField(QuienCertifica,verbose_name='¿Quién certifica?',blank=True)
	paga_certificacion = models.IntegerField(choices=PAGA_CERT_CHOICES,verbose_name='¿Quién paga la certificación?',blank=True,null=True)
	costo_certificacion = models.FloatField(verbose_name='¿Cuánto le cuesta estar certificado? (Lps)',blank=True,null=True)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "10.1 Tipo de certificación que posee"
		verbose_name_plural = "10.1 Tipo de certificación que posee"

class CostoProduccion(models.Model):
	mantenimiento_cacao = models.FloatField(verbose_name='Mantenimiento de área de cacao (Lps)')
	mantenimiento_finca = models.FloatField(verbose_name='Mantenimiento de la finca (Lps)')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "10.2 Costo de producción"
		verbose_name_plural = "10.2 Costo de producción"

VIVEROS_CHOICES = (
	(1,'Preparación del sitio'),
	(2,'Preparación del sustrato'),
	(3,'Llenado de bolsa'),
	(4,'Selección de semilla'),
	(5,'Siembra por semilla'),
	(6,'Uso de riego'),
	(7,'Control de malas hierba'),
	(8,'Fertilización orgánica'),
	(9,'Injertación'),
	)

FERTILIZACION_CHOICES = (
	(1,'Aplicación de té de estiércol'),
	(2,'Aplicación de gallinaza'),
	(3,'Aplicación de Bocashi'),
	(4,'Aplicación de foliares naturales'),
	(5,'Uso de triple cal'),
	(6,'Aplicación de lombrihumus'),
	(7,'Aplicación de urea'),
	(8,'Aplicación de fertilizante completo'),
	)

MANEJO_FIS_CHOICES = (
	(1,'Control de malas hierbas con machete'),
	(2,'Aplica herbicidas para controlar las malas hierbas'),
	(3,'Manejo de plagas con productos naturales'),
	(4,'Manejo de enfermedades con productos naturales'),
	(5,'Manejo de enfermedades con productos quimicos'),
	(6,'Recolección e eliminación de frutos enfermos'),
	)

MANEJO_PROD_CHOICES = (
	(1,'Poda de formación'),
	(2,'Poda de mantenimiento'),
	(3,'Poda de rehabilitación o renovación'),
	(4,'Regulación en sombra'),
	)

MEJORA_PLANTACION_CHOICES = (
	(1,'Selección de árboles superiores'),
	(2,'Injertación en árboles adultos'),
	(3,'Renovación de área con plantas injertadas'),
	(4,'Enriquecimiento de áreas con plantas injertadas'),
	)

MANEJO_POSTCOSECHA_CHOICES = (
	(1,'Selección y clasificación de mazorcas por variedad'),
	(2,'Selección de cacao en baba a fermentar'),
	(3,'Fermentación en sacos'),
	(4,'Fermentación en cajones'),
	(5,'Fermentación en cajillas'),
	(6,'Lo vende en baba a un centro de acopio'),
	(7,'Solo la saca de la mazorca y lo seca'),
	(8,'Lo saca de la mazorca, lo lava y luego lo seca'),
	)

class TecnicasAplicadas(models.Model):
	viveros = MultiSelectField(choices=VIVEROS_CHOICES,null=True,blank=True,verbose_name='11.1 Viveros')
	fertilizacion = MultiSelectField(choices=FERTILIZACION_CHOICES,verbose_name='11.2 Prácticas de fertilización',blank=True,null=True)
	pract_manejo_fis = MultiSelectField(choices=MANEJO_FIS_CHOICES,verbose_name='11.3 Prácticas de manejo fitosanitario',blank=True,null=True)
	pract_manejo_prod = MultiSelectField(choices=MANEJO_PROD_CHOICES,verbose_name='11.4 Prácticas de manejo productivo',blank=True,null=True)
	pract_mejora_plat = MultiSelectField(choices=MEJORA_PLANTACION_CHOICES,verbose_name='11.5 Prácticas de mejoramiento de la plantación',blank=True,null=True)
	pract_manejo_post_c = MultiSelectField(choices=MANEJO_POSTCOSECHA_CHOICES,verbose_name='11.6 Prácticas de manejo postcosecha y beneficiado',blank=True,null=True)
	acopio_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='11.7 Acopio de cacao en la comunidad/municipio')
	acopio_org = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='11.8 Asociación con Org. que acopia cacao')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "11 Técn. aplicadas área de cacao"
		verbose_name_plural = "11 Técn. aplicadas área de cacao"

PRODUCTO_CHOICES = (
	(1,'Mazorca de cacao (unidad)'),
	(2,'Semilla para siembra (unidad)'),
	(3,'Cacao en baba (qq)'),
	(4,'Cacao rojo sin fermentar (qq)'),
	(5,'Cacao fermentado (qq)'),
	(6,'Chocolate artesanal (lb)'),
	(7,'Cacao en polvo (lb)'),
	(8,'Cacao procesado (lb)'),
	(9,'Cajeta de cacao (lb)'),
	(10,'Pasta de cacao (lb)'),
	(11,'Vino de cacao (lt)'),
	)

QUIEN_VENDE_CHOICES = (
	(1,'Comunidad'),
	(2,'Intermediario'),
	(3,'Mercado'),
	(4,'Cooperativa'),
	)

class ComercializacionCacao(models.Model):
	producto = models.IntegerField(choices=PRODUCTO_CHOICES)
	auto_consumo = models.FloatField(verbose_name='Auto-consumo',blank=True, null=True)
	venta =  models.FloatField(blank=True, null=True)
	precio_venta = models.FloatField(verbose_name='Precio venta por unidad',blank=True, null=True)
	quien_vende = MultiSelectField(choices=QUIEN_VENDE_CHOICES,verbose_name='¿A quién le vende?',blank=True, null=True)
	donde_vende = models.ManyToManyField(Municipio,verbose_name='¿Dónde lo vende? Municipios',blank=True)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "12 Comercialización de cacao"
		verbose_name_plural = "12 Comercialización de cacao"

class DistanciaComercioCacao(models.Model):
	distancia = models.FloatField(verbose_name='Distancia (km)')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "12.1 Distancia recorrida"
		verbose_name_plural = "12.1 Distancia recorrida"

CAPACITACIONES_CHOICES = (
	(1,'Regular en sombra'),
	(2,'Poda'),
	(3,'Manejo de plagas y enfermedades'),
	(4,'Elaboración de abonos orgánicos'),
	(5,'Elaboración de productos para control de plagas'),
	(6,'Establecimiento de vivero'),
	(7,'Injertación de cacao'),
	(8,'Selección de árboles élites para producción de semillas'),
	(9,'Manejo de post-cosecha (selección, cosecha, fermentado, secado)'),
	(10,'Manejo de calidad de cacao'),
	(11,'Certificación orgánica'),
	)

OPCIONES_CAPACITACIONES_CHOICES = (
	(1,'Jefe familia varón'),
	(2,'Jefa familia mujer'),
	(3,'Hijos'),
	(4,'Hijas'),
	)

class CapacitacionesTecnicas(models.Model):
	capacitaciones = models.IntegerField(choices=CAPACITACIONES_CHOICES)
	opciones = MultiSelectField(choices=OPCIONES_CAPACITACIONES_CHOICES)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "13.1 Capacitación familia"
		verbose_name_plural = "13.1 Capacitaciones familia"

CAPACITACIONES_SOCIO_CHOICES = (
	(1,'Formación y fortalecimiento organizacional'),
	(2,'Contabilidad básica y administración'),
	(3,'Equidad de género'),
	(4,'Manejo de créditos'),
	(5,'Administración de pequeños negocios'),
	(6,'Gestión empresarial'),
	(7,'Cadena de valor de cacao'),
	(8,'Transformación de cacao'),
	)


class CapacitacionesSocioeconomicas(models.Model):
	capacitaciones_socio = models.IntegerField(choices=CAPACITACIONES_SOCIO_CHOICES,verbose_name='Capacitaciones')
	opciones_socio = MultiSelectField(choices=OPCIONES_CAPACITACIONES_CHOICES,verbose_name='Opciones')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "13.2 Capacitaciones socioeconómico/org"
		verbose_name_plural = "13.2 Capacitaciones socioeconómico/org"

class ProblemasAreaCacao(models.Model):
	area_1 = models.ManyToManyField(ProblemasArea1,verbose_name='En áreas de 1 a 3 años')
	area_2 = models.ManyToManyField(ProblemasArea2,verbose_name='En áreas de 4 a 10 años')
	area_3 = models.ManyToManyField(ProblemasArea3,verbose_name='En áreas de 10 a 20 años')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "13.3 Principales problemas áreas de cacao"
		verbose_name_plural = "13.3 Principales problemas áreas de cacao"

DECISIONES_CHOICES = (
	(1,'Decide Usted sobre la siembra de cacao'),
	(2,'Decide Usted sobre la cosecha de cacao'),
	(3,'Decide Usted sobre la venta de cacao'),
	(4,'Decide Usted sobre la Ingresos de cacao'),
	)

class Genero(models.Model):
	actividades = models.ManyToManyField(ActividadesProduccion,verbose_name='Actividades en las que participa',blank=True,)
	ingresos = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Recibe ingresos por las actividades que realiza?')
	ingreso_mesual_cacao = models.FloatField(null=True,blank=True,verbose_name='Ingreso mensual aproximado percibido (solo por cacao)')
	ingreso_mesual = models.FloatField(null=True,blank=True,verbose_name='Ingreso mensual aproximado percibido (incluyendo todas las actividades)')
	destino_ingresos = models.ManyToManyField(DestinoIngresos,verbose_name='Destino de los ingresos percibidos',blank=True)
	decisiones = MultiSelectField(choices=DECISIONES_CHOICES,verbose_name='Decisiones sobre destino de la producción',blank=True,null=True)
	otros_ingresos = models.ManyToManyField(OtrosIngresos,verbose_name='Sobre otros Ingresos')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "14 Género"
		verbose_name_plural = "14 Género"

class AmpliarAreasCacao(models.Model):
	interes = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Tiene interes en ampliar las áreas de cacao')
	cuanto = models.FloatField(verbose_name='Cuantas manzanas')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "15 Amplición áreas de cacao"
		verbose_name_plural = "15 Amplición áreas de cacao"
