# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SistemaInfo(models.Model):
    texto = models.TextField()

    class Meta:
        verbose_name_plural = "Texto Sistema de Información"

class InfoGeneral(models.Model):
    texto = models.TextField()

    class Meta:
        verbose_name_plural = "Texto Sistema de la Asociación de Productores"

class Objetivo(models.Model):
    texto = models.TextField()

    class Meta:
        verbose_name_plural = "Objetivo"

class Alcance(models.Model):
    texto = models.TextField()

    class Meta:
        verbose_name_plural = "Alcance"

class Actualizacion(models.Model):
    texto = models.TextField()

    class Meta:
        verbose_name_plural = "Actualización"
