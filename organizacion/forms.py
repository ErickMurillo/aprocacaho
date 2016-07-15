# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms

STATUS_CHOICES = (('','Todos'),(1,'ONG'),(2, 'Cooperativa'),(3, 'Unión de Cooperativa'))

class EncuestaOrgConsulta(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EncuestaOrgConsulta, self).__init__(*args, **kwargs)
        self.fields['status'] = forms.ChoiceField(label=u'Estatus',choices=STATUS_CHOICES,required=False)
