# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from lugar.models import *
from sorl.thumbnail import ImageField
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
STATUS_CHOICES = (
	(1,'Asociación Sin Fin de lucro'),
	(2,'Cooperación técnica y/o financiera'),
	(3, 'Cooperativa'),
	(4, 'Institución del estado'),
	(5, 'Unión de Cooperativa'),
	)

class Organizacion(models.Model):
	nombre = models.CharField(max_length=200,verbose_name='Nombre de la Organización')
	siglas = models.CharField(max_length=200)
	gerente = models.CharField(max_length=200,verbose_name='Representante legal',null=True,blank=True)
	status = models.IntegerField(verbose_name='Estatus Legal',choices=STATUS_CHOICES)
	fundacion = models.DateField(verbose_name='Año de fundación',null=True,blank=True)
	direccion = models.CharField(max_length=300,null=True,blank=True)
	departamento = models.ForeignKey(Departamento)
	municipio = ChainedForeignKey(
                                Municipio,
                                chained_field="departamento",
                                chained_model_field="departamento",
                                show_all=False, auto_choose=True)
	telefono = models.IntegerField(verbose_name='Número telefónico',null=True,blank=True)
	fax = models.IntegerField(verbose_name='Número fax',null=True,blank=True)
	email = models.EmailField(null=True,blank=True)
	web = models.URLField(verbose_name='Página web',null=True,blank=True)
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
