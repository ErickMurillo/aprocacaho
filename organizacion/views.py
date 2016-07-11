# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from .forms import *
import json as simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Sum, Count, Avg
import collections

# Create your views here.
def detail_org(request,template = 'organizaciones/detalle.html',slug = None):
    object = Organizacion.objects.filter(slug = slug)
    encuesta = EncuestaOrganicacion.objects.filter(organizacion__slug = slug)
    years = collections.OrderedDict()

    years_list = EncuestaOrganicacion.objects.filter(organizacion__slug = slug).order_by('anno').values_list('anno', flat=True).distinct('anno')

    for year in years_list:
        aspectos_juridicos = []
        for obj in AspectosJuridicos.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            aspectos_juridicos.append((obj.get_tiene_p_juridica_display(),
                                        obj.get_solvencia_tributaria_display(),
                                        obj.get_junta_directiva_display(),
                                        obj.mujeres,
                                        obj.hombres,
                                        obj.get_lista_socios_display(),
                                        obj.numero_registro,
                                        ))

        lista_miembros = []
        for obj in ListaMiembros.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            lista_miembros.append((obj.nombre,obj.cargo,obj.telefonos))


        documentos = []
        for obj in Documentacion.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            documentos.append((obj.get_documentos_display(),obj.get_si_no_display(),obj.tramite,obj.fecha))

        cumplimiento = []
        for obj in NivelCumplimiento.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            cumplimiento.append((obj.get_documentos_display(),obj.get_cumplimiento_display()))

        datos_productivos = []
        for obj in DatosProductivos.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            datos_productivos.append((obj.get_pregunta_display(),
                                        obj.productores_socios,
                                        obj.productoras_socias,
                                        obj.productores_no_socios,
                                        obj.productoras_no_socias
                                    ))

        datos = []
        for obj in DatosProductivosTabla.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            datos.append((obj.get_pregunta_display(),obj.productores_socios,obj.productores_no_socios))

        years[year] = (aspectos_juridicos,lista_miembros,documentos,cumplimiento,datos_productivos,
                        datos)

    return render(request, template, locals())

def consulta_org(request,template="organizaciones/consulta.html"):
    if request.method == 'POST':
        mensaje = None
        form = EncuestaOrgConsulta(request.POST)
        if form.is_valid():
            request.session['status'] = form.cleaned_data['status']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

            status = request.session['status']
            if status != '':
                list_municipio = Organizacion.objects.filter(status = status).values_list('municipio', flat = True).distinct('municipio')
                lista = []
                for x in list_municipio:
                    municipio = Municipio.objects.filter(id = x)
                    organizaciones = Organizacion.objects.filter(municipio = x,status = status)
                    for y in municipio:
                        lista.append((y,float(y.latitud),float(y.longitud),organizaciones))
                municipios = lista
            else:
                list_municipio = Organizacion.objects.values_list('municipio', flat=True).distinct('municipio')
                lista = []
                for x in list_municipio:
                    municipio = Municipio.objects.filter(id = x)
                    organizaciones = Organizacion.objects.filter(municipio = x)
                    for y in municipio:
                        lista.append((y,float(y.latitud),float(y.longitud),organizaciones))
                municipios = lista

    else:
        form = EncuestaOrgConsulta()
        mensaje = "Existen alguno errores"
        centinela = 0

        list_municipio = Organizacion.objects.values_list('municipio', flat = True).distinct('municipio')
        lista = []
        for x in list_municipio:
            municipio = Municipio.objects.filter(id = x)
            organizaciones = Organizacion.objects.filter(municipio = x)
            for y in municipio:
                lista.append((y,float(y.latitud),float(y.longitud),organizaciones))
        municipios = lista

        try:
            del request.session['status']
        except:
            pass

    return render(request, template, locals())
