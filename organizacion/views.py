# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from .forms import *
import json as simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Sum, Count, Avg
import collections
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
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
                list_municipio = Organizacion.objects.filter(status = status).values_list('municipio', flat = True).distinct()
                lista = []
                for x in list_municipio:
                    municipio = Municipio.objects.filter(id = x)
                    organizaciones = Organizacion.objects.filter(municipio = x,status = status)
                    for y in municipio:
                        lista.append((y,float(y.latitud),float(y.longitud),organizaciones))
                municipios = lista
            else:
                list_municipio = Organizacion.objects.values_list('municipio', flat=True).distinct()
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

        list_municipio = Organizacion.objects.values_list('municipio', flat = True).distinct()
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

@login_required
def detail_org(request,template = 'organizaciones/detalle.html',slug = None):
    object = Organizacion.objects.filter(slug = slug)
    years = collections.OrderedDict()

    years_list = EncuestaOrganicacion.objects.filter(organizacion__slug = slug).order_by('anno').values_list('anno', flat=True).distinct()

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

@login_required
def estatus_legal(request,template="organizaciones/estatus_legal.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()

    STATUS_CHOICES = ((1,'ONG'),(2, 'Cooperativa'),(3, 'Unión de Cooperativa'))

    for year in years_encuesta:
        status = {}
        org_by_status = {}
        for obj in STATUS_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(organizacion__status = obj[0],anno = year).count()
            status[obj[1]] = conteo

            name_org = EncuestaOrganicacion.objects.filter(organizacion__status = obj[0],anno = year)
            org_by_status[obj[1]] = name_org

        years[year] = (status,org_by_status)

    return render(request, template, locals())

@login_required
def aspectos_juridicos(request,template="organizaciones/aspectos_juridicos.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()
    STATUS_CHOICES = ((1,'ONG'),(2, 'Cooperativa'),(3, 'Unión de Cooperativa'))

    for year in years_encuesta:
        count_org = EncuestaOrganicacion.objects.filter(anno = year).distinct('organizacion__nombre').count()
        lista_hombres = []
        lista_mujeres = []
        graf_bar_status = {}
        for obj in STATUS_CHOICES:
            mujeres =  EncuestaOrganicacion.objects.filter(organizacion__status = obj[0],anno = year).aggregate(
                                                            total = Sum('aspectosjuridicos__mujeres'))['total']
            if mujeres == None:
                mujeres = 0

            hombres = EncuestaOrganicacion.objects.filter(organizacion__status = obj[0],anno = year).aggregate(
                                                            total = Sum('aspectosjuridicos__hombres'))['total']
            if hombres == None:
                hombres = 0

            lista_hombres.append([obj[1],hombres])
            lista_mujeres.append([obj[1],mujeres])

        graf_bar_status['Hombres'] = lista_hombres
        graf_bar_status['Mujeres'] = lista_mujeres

        #----------------------------------------------------------------------------
        juridica = {}
        for obj in TRAMITE_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(aspectosjuridicos__tiene_p_juridica = obj[0],anno = year).count()
            juridica[obj[1]] = conteo

        #----------------------------------------------------------------------------
        aspectos_juridicos = {}
        tabla_aspectos_juridicos = {}
        for obj in SI_NO_CHOICES:
            solvencia_tributaria = EncuestaOrganicacion.objects.filter(aspectosjuridicos__solvencia_tributaria = obj[0],anno = year)
            count_solvencia = solvencia_tributaria.count()

            junta_directiva = EncuestaOrganicacion.objects.filter(aspectosjuridicos__junta_directiva = obj[0],anno = year)
            count_junta_directiva = junta_directiva.count()

            socios = EncuestaOrganicacion.objects.filter(aspectosjuridicos__lista_socios = obj[0],anno = year)
            count_socios = socios.count()

            lista = [
					saca_porcentajes(count_solvencia,count_org,False),
					saca_porcentajes(count_junta_directiva,count_org,False),
					saca_porcentajes(count_socios,count_org,False)
                    ]

            lista_org = [solvencia_tributaria,junta_directiva,socios]

            aspectos_juridicos[obj[1]] = lista
            tabla_aspectos_juridicos[obj[1]] = lista_org

        years[year] = (graf_bar_status,juridica,aspectos_juridicos,tabla_aspectos_juridicos)

    return render(request, template, locals())

@login_required
def documentacion(request,template="organizaciones/documentacion.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()
    for year in years_encuesta:
        documentacion = {}
        tabla_documantacion = {}
        count_org = EncuestaOrganicacion.objects.filter(anno = year).distinct('organizacion__nombre').count()
        for x in SI_NO_CHOICES:
            documentos = {}
            tabla_documentos = {}
            for obj in DOCUMENTOS_CHOICES:
                result = EncuestaOrganicacion.objects.filter(documentacion__documentos = obj[0],documentacion__si_no = x[0],anno = year)
                count_result = result.count()
                documentos[obj[1]] = saca_porcentajes(count_result,count_org,False)
                tabla_documentos[obj[1]] = result

            documentacion[x[1]] = documentos
            tabla_documantacion[x[1]] = tabla_documentos

        years[year] = (documentacion,tabla_documantacion)

    return render(request, template, locals())

@login_required
def datos_productivos(request,template="organizaciones/datos_productivos.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()
    for year in years_encuesta:
        count_org = EncuestaOrganicacion.objects.filter(anno = year).distinct('organizacion__nombre').count()
        areas_socios = []
        areas_no_socios = []
        for obj in DATOS_PROD_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(datosproductivos__pregunta = obj[0],anno = year).aggregate(
                                                        socios = Sum('datosproductivos__productores_socios'),
                                                        avg_socios = Avg('datosproductivos__productores_socios'),
                                                        socias = Sum('datosproductivos__productoras_socias'),
                                                        avg_socias = Avg('datosproductivos__productoras_socias'),
                                                        no_socios = Sum('datosproductivos__productores_no_socios'),
                                                        avg_no_socios = Avg('datosproductivos__productores_no_socios'),
                                                        no_socias = Sum('datosproductivos__productoras_no_socias'),
                                                        avg_no_socias = Avg('datosproductivos__productoras_no_socias'))
            if obj[0] == 1:
                lista_socios = [conteo['socios'],conteo['socias'],conteo['no_socios'],conteo['no_socias']]
            else:
                areas_socios.append((obj[1],conteo['socios'],conteo['avg_socios'],conteo['socias'],conteo['avg_socias']))

                areas_no_socios.append((obj[1],conteo['no_socios'],conteo['avg_no_socios'],conteo['no_socias'],conteo['avg_no_socias']))

        years[year] = (lista_socios,areas_socios,areas_no_socios)

    return render(request, template, locals())

@login_required
def instalaciones(request,template="organizaciones/instalaciones.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()
    for year in years_encuesta:
        infraestructura = []
        for obj in INFRAESTRUCTURA_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(infraestructura__tipo = obj[0],anno = year).aggregate(
                                                        total = Count('infraestructura__tipo'),
                                                        capacidad = Sum('infraestructura__capacidad'),
                                                        avg_capacidad = Avg('infraestructura__capacidad'))

            estado = []
            for x in ESTADO_CHOICES:
                qs = EncuestaOrganicacion.objects.filter(infraestructura__estado = x[0],infraestructura__tipo = obj[0],anno = year).count()
                estado.append((saca_porcentajes(qs,conteo['total'],False)))

            infraestructura.append((obj[1],conteo['total'],conteo['capacidad'],conteo['avg_capacidad'],estado))

        transporte = {}
        for obj in SI_NO_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(transporte__medio_transporte = obj[0],anno = year).count()
            transporte[obj[1]] = conteo

        estado_transporte = {}
        for obj in ESTADO_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(transporte__estado = obj[0],anno = year).count()
            estado_transporte[obj[1]] = conteo

        years[year] = (infraestructura,transporte,estado_transporte)

    return render(request, template, locals())

@login_required
def comercializacion(request,template="organizaciones/comercializacion.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()
    for year in years_encuesta:
        lista_corriente = []
        lista_fermentado = []
        count_org = EncuestaOrganicacion.objects.filter(anno = year).distinct('organizacion__nombre').count()
        for obj in COMERCIO_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(comercializacion__seleccion = obj[0],anno = year).aggregate(
                                                        socias_corriente = Sum('comercializacion__socias_corriente'),
                                                        avg_socias_corriente = Avg('comercializacion__socias_corriente'),
                                                        socios_corriente = Sum('comercializacion__socios_corriente'),
                                                        avg_socios_corriente = Avg('comercializacion__socios_corriente'),
                                                        socias_fermentado = Sum('comercializacion__no_socias_corriente'),
                                                        avg_socias_fermentado = Avg('comercializacion__no_socias_corriente'),
                                                        socios_fermentado = Sum('comercializacion__no_socios_corriente'),
                                                        avg_socios_fermentado = Avg('comercializacion__no_socios_corriente'))

            lista_corriente.append((
                                    obj[1],
                                    conteo['socias_corriente'],
                                    conteo['avg_socias_corriente'],
                                    conteo['socios_corriente'],
                                    conteo['avg_socios_corriente'],
                                    ))

            lista_fermentado.append((
                                    obj[1],
                                    conteo['socias_fermentado'],
                                    conteo['avg_socias_fermentado'],
                                    conteo['socios_fermentado'],
                                    conteo['avg_socios_fermentado'],
                                    ))
            #--------------------------------------------------------
            #comercio org, bar graf
            corriente = EncuestaOrganicacion.objects.filter(anno = year).aggregate(total = Sum('cacaocomercializado__corriente'))['total']
            fermentado = EncuestaOrganicacion.objects.filter(anno = year).aggregate(total = Sum('cacaocomercializado__fermentado'))['total']

            #--------------------------------------------------------
            #certificacion
            certificacion = {}
            for obj in CERTIFICACION_CHOICES:
                cert_corriente = EncuestaOrganicacion.objects.filter(certificacionorg__corriente__icontains = obj[0],anno = year).count()
                cert_fermentado = EncuestaOrganicacion.objects.filter(certificacionorg__fermentado__icontains = obj[0],anno = year).count()

                certificacion[obj[1]] = (saca_porcentajes(cert_corriente,count_org,False),saca_porcentajes(cert_fermentado,count_org,False))

            #--------------------------------------------------------
            #destino produccion
            destino_prod = {}
            for obj in DESTINO_CHOICES:
                destino_corriente = EncuestaOrganicacion.objects.filter(destinoprodcorriente__destino = obj[0],anno = year).count()
                destino_fermentado = EncuestaOrganicacion.objects.filter(destinoprodfermentado__destino = obj[0],anno = year).count()

                destino_prod[obj[1]] = (saca_porcentajes(destino_corriente,count_org,False),saca_porcentajes(destino_fermentado,count_org,False))

        years[year] = (lista_corriente,lista_fermentado,corriente,fermentado,certificacion,destino_prod)

    return render(request, template, locals())

def financiamiento_produccion(request,template="organizaciones/financiamiento_produccion.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()
    for year in years_encuesta:
        count_org = EncuestaOrganicacion.objects.filter(anno = year).distinct('organizacion__nombre').count()

        financiamiento = {}
        for obj in SI_NO_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(financiamiento__financiamiento = obj[0],anno = year).count()
            financiamiento[obj[1]] = conteo

        tipo_financiamiento = {}
        monto = []
        for obj in TIPO_FINANCIAM_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(financiamientoproductores__tipo = obj[0],anno = year).count()
            tipo_financiamiento[obj[1]] = saca_porcentajes(conteo,count_org,False)

            calc_monto = EncuestaOrganicacion.objects.filter(financiamientoproductores__tipo = obj[0],anno = year).aggregate(
                                                            total = Sum('financiamientoproductores__monto'),
                                                            avg = Avg('financiamientoproductores__monto'))
            monto.append((obj[1],calc_monto['total'],calc_monto['avg']))

        years[year] = (financiamiento,tipo_financiamiento,monto)

    return render(request, template, locals())

def financiamiento_organizacion(request,template="organizaciones/financiamiento_organizacion.html"):
    years_encuesta = EncuestaOrganicacion.objects.all().values_list('anno', flat=True)

    years = collections.OrderedDict()
    for year in years_encuesta:
        count_org = EncuestaOrganicacion.objects.filter(anno = year).distinct('organizacion__nombre').count()

        financiamiento_org = {}
        for obj in FINANACIA_CHOICES:
            conteo = EncuestaOrganicacion.objects.filter(infofinanciamiento__seleccion = obj[0],anno = year).count()
            financiamiento_org[obj[1]] = saca_porcentajes(conteo,count_org,False)

        years[year] = financiamiento_org

    return render(request, template, locals())

#utils
def saca_porcentajes(dato, total, formato=True):
	if dato != None:
		try:
			porcentaje = (dato/float(total)) * 100 if total != None or total != 0 else 0
		except:
			return 0
		if formato:
			return porcentaje
		else:
			return '%.2f' % porcentaje
	else:
		return 0

def indicadores(request, template="organizaciones/indicadores.html"):
    return render(request, template, locals())