# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from .forms import *
import json as simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Sum, Count, Avg
import collections

# Create your views here.
def _queryset_filtrado(request):
	params = {}

	if request.session['year']:
		params['year__in'] = request.session['year']

	if request.session['departamento']:
		if not request.session['municipio']:
			municipios = Municipio.objects.filter(departamento__in=request.session['departamento'])
			params['persona__comunidad__municipio__in'] = municipios
		else:
			if request.session['comunidad']:
				params['persona__comunidad__in'] = request.session['comunidad']
			else:
				params['persona__comunidad__municipio__in'] = request.session['municipio']

	if request.session['organizacion']:
		params['organizacion'] = request.session['organizacion']

	if request.session['socio']:
		params['organizacionasociada__socio'] = request.session['socio']


	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return Encuesta.objects.filter(**params).order_by('year')

def consulta_productores(request,template="productores/consulta.html"):
	if request.method == 'POST':
		mensaje = None
		form = EncuestaConsulta(request.POST)
		if form.is_valid():
			request.session['year'] = form.cleaned_data['year']
			request.session['departamento'] = form.cleaned_data['departamento']
			request.session['municipio'] = form.cleaned_data['municipio']
			request.session['comunidad'] = form.cleaned_data['comunidad']
			request.session['organizacion'] = form.cleaned_data['organizacion']
			request.session['socio'] = form.cleaned_data['socio']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1

			return HttpResponseRedirect('/productores/dashboard/')

		else:
			centinela = 0

	else:
		form = EncuestaConsulta()
		mensaje = "Existen alguno errores"
		centinela = 0
		try:
			del request.session['year']
			del request.session['departamento']
			del request.session['municipio']
			del request.session['comunidad']
			del request.session['organizacion']
			del request.session['socio']
		except:
			pass

	return render(request, template, locals())

def dashboard(request,template="productores/dashboard.html"):
    filtro = _queryset_filtrado(request)

    years = collections.OrderedDict()

    for year in request.session['year']:
        productores = filtro.filter(year=year).count()
        #plantacion cacao
        areas = collections.OrderedDict()
        area_total = filtro.filter(year=year).aggregate(area_total=Sum('plantacion__area'))['area_total']

        for obj in EDAD_PLANTA_CHOICES:
			conteo = filtro.filter(year=year,plantacion__edad=obj[0]).aggregate(total=Sum('plantacion__area'))['total']
			if conteo == None:
				conteo = 0
			areas[obj[1]] = saca_porcentajes(conteo,area_total,False)

        #rendimiento
        #areas certificadas
        area_cert = filtro.filter(year=year,plantacion__edad__in=[3,4,5],certificacion__cacao_certificado='1').aggregate(area_cacao=Sum('plantacion__area'))['area_cacao']
        if area_cert == None:
        	area_cert = 0

        #areas no certificadas
        area_no_cert = filtro.filter(year=year,plantacion__edad__in=[3,4,5],certificacion__cacao_certificado='2').aggregate(area_cacao=Sum('plantacion__area'))['area_cacao']
        if area_no_cert == None:
        	area_no_cert = 0

        convencional = filtro.filter(year=year,certificacion__cacao_certificado='2').aggregate(convencional=Sum('produccioncacao__cacao_baba'))['convencional']
        if convencional == None:
        	convencional = 0

        fermentado = filtro.filter(year=year,certificacion__cacao_certificado='1').aggregate(fermentado=Sum('produccioncacao__cacao_baba'))['fermentado']
        if fermentado == None:
        	fermentado = 0

        try:
        	rendimiento_conv = (convencional * 100) / area_no_cert
        except:
        	rendimiento_conv = 0

        try:
        	rendimiento_ferm = (fermentado * 100) / area_cert
        except:
        	rendimiento_ferm = 0

        #area total
        area_total = filtro.filter(year=year).aggregate(area_total=Sum('plantacion__area'))['area_total']

        #promedio mz x productor
        promedio_productor = filtro.filter(year=year).aggregate(avg_cacao=Avg('areacacao__area'))['avg_cacao']
        if promedio_productor == None:
            promedio_productor = 0

        #productores socios y no socios
        socio = (filtro.filter(year=year,organizacionasociada__socio='1').count() / float(productores)) * 100
        if socio == None:
            socio = 0

        no_socio = (filtro.filter(year=year,organizacionasociada__socio='2').count() / float(productores)) * 100
        if no_socio == None:
            no_socio = 0

        #productores certificados y no certificados
    	certificados = filtro.filter(year=year,certificacion__cacao_certificado = 1).count()
    	no_certificados = filtro.filter(year=year,certificacion__cacao_certificado = 2).count()

        #No de productores con uno o más sellos
    	conteo_1 = 0
    	conteo_2 = 0
    	conteo_3 = 0
    	lista_certificaciones = []
    	for obj in filtro:
    		certificaciones = 0
    		for x in Certificacion.objects.filter(encuesta__year=year,cacao_certificado=1,encuesta=obj):
    			for z in x.tipo.all():
    				certificaciones += 1
    		if certificaciones == 1:
    			conteo_1 += 1
    		elif certificaciones == 2:
    			conteo_2 += 1
    		elif certificaciones > 2:
    			conteo_3 += 1
    	lista_certificaciones.append([conteo_1, conteo_2, conteo_3])
        for list in lista_certificaciones:
            print list[0]
        #diccionario de los años
        years[year] = (areas,rendimiento_conv,rendimiento_ferm,convencional,fermentado,area_total,promedio_productor,
                        socio,no_socio,certificados,no_certificados,lista_certificaciones)

    return render(request, template, locals())

def get_munis(request):
	'''Metodo para obtener los municipios via Ajax segun los departamentos selectos'''
	ids = request.GET.get('ids', '')
	dicc = {}
	resultado = []
	if ids:
		lista = ids.split(',')
		for id in lista:
			try:
				encuesta = Encuesta.objects.filter(entrevistado__municipio__departamento__id=id).distinct().values_list('entrevistado__municipio__id', flat=True)
				departamento = Departamento.objects.get(pk=id)
				municipios = Municipio.objects.filter(departamento__id=departamento.pk,id__in=encuesta).order_by('nombre')
				lista1 = []
				for municipio in municipios:
					muni = {}
					muni['id'] = municipio.pk
					muni['nombre'] = municipio.nombre
					lista1.append(muni)
					dicc[departamento.nombre] = lista1
			except:
				pass

	#filtrar segun la organizacion seleccionada
	org_ids = request.GET.get('org_ids', '')
	if org_ids:
		lista = org_ids.split(',')
		municipios = [encuesta.municipio for encuesta in Encuesta.objects.filter(organizacion__id__in=lista)]
		#crear los keys en el dicc para evitar KeyError
		for municipio in municipios:
			dicc[municipio.departamento.nombre] = []

		#agrupar municipios por departamento padre
		for municipio in municipios:
			muni = {'id': municipio.id, 'nombre': municipio.nombre}
			if not muni in dicc[municipio.departamento.nombre]:
				dicc[municipio.departamento.nombre].append(muni)

	resultado.append(dicc)

	return HttpResponse(simplejson.dumps(resultado), content_type='application/json')

def get_comunies(request):
	ids = request.GET.get('ids', '')
	if ids:
		lista = ids.split(',')
	results = []
	comunies = Comunidad.objects.filter(municipio__pk__in=lista).order_by('nombre').values('id', 'nombre')

	return HttpResponse(simplejson.dumps(list(comunies)), content_type='application/json')

def get_organi(request):
	ids = request.GET.get('ids', '')
	if ids:
		lista = ids.split(',')
	organizaciones = Organizacion.objects.filter(departamento__id__in = lista).order_by('nombre').values('id', 'siglas')

	return HttpResponse(simplejson.dumps(list(organizaciones)), content_type='application/json')

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
