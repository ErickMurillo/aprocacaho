from django.shortcuts import render
from productores.models import *
from organizacion.models import *
from django.db.models import Sum, Count, Avg

def index(request,template="index.html"):
    socios = Encuesta.objects.filter(organizacionasociada__socio = '1').count()
    socios_mujeres = Encuesta.objects.filter(organizacionasociada__socio = '1',entrevistado__sexo = '1').count()
    socios_hombres = Encuesta.objects.filter(organizacionasociada__socio = '1',entrevistado__sexo = '2').count()

    organizaciones = Encuesta.objects.all().order_by('organizacion__nombre').distinct('organizacion__nombre').count()

    return render(request, template, locals())
