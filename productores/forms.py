# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms

def fecha_choice():
    years = []
    for en in Encuesta.objects.order_by('year').values_list('year', flat=True):
        years.append((en,en))
    return list(sorted(set(years)))

def departamentos():
    foo = Encuesta.objects.all().order_by('entrevistado__comunidad__municipio__departamento__nombre').distinct().values_list('entrevistado__comunidad__municipio__departamento__id', flat=True)
    return Departamento.objects.filter(id__in=foo)

def organizaciones():
    foo = Encuesta.objects.all().order_by('organizacion').distinct().values_list('organizacion', flat=True)
    return Organizacion.objects.filter(id__in=foo)

SI_NO_CHOICE = (('','----'),(1,'Si'),(2,'No'))

class EncuestaConsulta(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EncuestaConsulta, self).__init__(*args, **kwargs)
        self.fields['year'] = forms.MultipleChoiceField(choices=fecha_choice(),required=True,label=u'Años')
        self.fields['departamento'] = forms.ModelMultipleChoiceField(queryset=departamentos(), required=False, label=u'Departamentos')
        self.fields['municipio'] = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all().order_by('nombre'), required=False)
        self.fields['comunidad'] = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(), required=False)
        self.fields['organizacion'] = forms.ModelMultipleChoiceField(queryset=organizaciones(),required=False)
        self.fields['socio'] = forms.ChoiceField(label=u'Socios',choices=SI_NO_CHOICE,required=False)
