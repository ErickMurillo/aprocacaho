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
    # encuesta = EncuestaOrganicacion.objects.filter(organizacion__slug = slug)
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

        infraestructura = []
        for obj in Infraestructura.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            infraestructura.append((obj.get_tipo_display(),
                                    obj.capacidad,
                                    obj.anno_construccion,
                                    obj.get_estado_display()
                                    ))

        transporte = []
        for obj in Transporte.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            transporte.append((obj.get_medio_transporte_display(),obj.get_estado_display))

        comercio = []
        for obj in Comercializacion.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            comercio.append((obj.get_seleccion_display,
                            obj.socias_corriente,
                            obj.socios_corriente,
                            obj.no_socias_corriente,
                            obj.no_socios_corriente
                            ))

        cacao_seco = []
        for obj in CacaoComercializado.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            cacao_seco.append((obj.corriente,obj.fermentado))

        certificacion = []
        for obj in CertificacionOrg.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            certificacion.append((obj.get_corriente_display(),obj.get_fermentado_display()))

        destino_corriente = []
        for obj in DestinoProdCorriente.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            destino_corriente.append((obj.get_destino_display(),obj.entrega))

        destino_fermentado = []
        for obj in DestinoProdFermentado.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            destino_fermentado.append((obj.get_destino_display(),obj.entrega))

        financiamiento = ''
        for obj in Financiamiento.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            financiamiento = obj.get_financiamiento_display()

        tipo_financiamiento = []
        for obj in FinanciamientoProductores.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            tipo_financiamiento.append((obj.get_tipo_display(),obj.monto))

        financia_org = []
        for obj in InfoFinanciamiento.objects.filter(encuesta__anno = year,encuesta__organizacion__slug = slug):
            financia_org.append((obj.get_seleccion_display(),obj.monto,obj.porcentaje))

        years[year] = (aspectos_juridicos,lista_miembros,documentos,cumplimiento,datos_productivos,
                        datos,infraestructura,transporte,comercio,cacao_seco,certificacion,destino_corriente,
                        destino_fermentado,financiamiento,tipo_financiamiento,financia_org)

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
