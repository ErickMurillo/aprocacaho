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
			params['entrevistado__comunidad__municipio__in'] = municipios
		else:
			if request.session['comunidad']:
				params['entrevistado__comunidad__in'] = request.session['comunidad']
			else:
				params['entrevistado__comunidad__municipio__in'] = request.session['municipio']

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
		if certificados == None:
			certificados = 0
		no_certificados = filtro.filter(year=year,certificacion__cacao_certificado = 2).count()
		if no_certificados == None:
			no_certificados = 0

		# #No de productores con uno o más sellos
		x = 0
		y = 0
		z = 0
		lista_certificaciones = []
		for obj in filtro.filter(year=year):
			num_certif = 0
			for cert in Certificacion.objects.filter(cacao_certificado=1,encuesta=obj):
				for tipo in cert.tipo:
					num_certif += 1
			if num_certif == 1:
				x += 1
			elif num_certif == 2:
				y += 1
			elif num_certif > 2:
				z += 1
		lista_certificaciones.append([x, y, z])

		prod_depto = {}
		for depto in Departamento.objects.all():
			produccion = filtro.filter(year=year,entrevistado__departamento=depto).aggregate(total=Sum('produccioncacao__cacao_baba'))['total']
			if produccion == None:
				produccion = 0

			if produccion != 0:
				prod_depto[depto] = (depto.latitud_1,depto.longitud_1,produccion)

		#diccionario de los años
		years[year] = (areas,rendimiento_conv,rendimiento_ferm,convencional,fermentado,area_total,promedio_productor,
						socio,no_socio,certificados,no_certificados,lista_certificaciones,prod_depto)

	return render(request, template, locals())

def educacion(request,template="productores/educacion.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	lista_hombres = [1,3,5,7,9]
	lista_mujeres = [2,4,6,8,10]
	for year in request.session['year']:
		#hombres
		cantidad_miembros_hombres = filtro.filter(year=year,educacion__rango__in=lista_hombres).aggregate(
									num_total = Sum('educacion__numero_total'))['num_total']

		grafo_educacion_hombre = filtro.filter(year=year,educacion__rango__in=lista_hombres).aggregate(
									no_lee_ni_escribe = Sum('educacion__no_lee_ni_escribe'),
									primaria_incompleta = Sum('educacion__primaria_incompleta'),
									primaria_completa = Sum('educacion__primaria_completa'),
									secundaria_incompleta = Sum('educacion__secundaria_incompleta'),
									bachiller = Sum('educacion__bachiller'),
									universitario = Sum('educacion__universitario_tecnico'))

		#mujeres
		cantidad_miembros_mujeres = filtro.filter(year=year,educacion__rango__in=lista_mujeres).aggregate(
									num_total = Sum('educacion__numero_total'))['num_total']

		grafo_educacion_mujer = filtro.filter(year=year,educacion__rango__in=lista_mujeres).aggregate(
									no_lee_ni_escribe = Sum('educacion__no_lee_ni_escribe'),
									primaria_incompleta = Sum('educacion__primaria_incompleta'),
									primaria_completa = Sum('educacion__primaria_completa'),
									secundaria_incompleta = Sum('educacion__secundaria_incompleta'),
									bachiller = Sum('educacion__bachiller'),
									universitario = Sum('educacion__universitario_tecnico'))

		#tablas
		tabla_educacion_hombre = []
		tabla_educacion_mujer = []
		for e in RANGOS_CHOICE:
			objeto = filtro.filter(year=year, educacion__rango = e[0]).aggregate(num_total = Sum('educacion__numero_total'),
									no_lee_ni_escribe = Sum('educacion__no_lee_ni_escribe'),
									primaria_incompleta = Sum('educacion__primaria_incompleta'),
									primaria_completa = Sum('educacion__primaria_completa'),
									secundaria_incompleta = Sum('educacion__secundaria_incompleta'),
									bachiller = Sum('educacion__bachiller'),
									universitario = Sum('educacion__universitario_tecnico'))

			fila = [e[1], objeto['num_total'],
				saca_porcentajes(objeto['no_lee_ni_escribe'], objeto['num_total'], False),
				saca_porcentajes(objeto['primaria_incompleta'], objeto['num_total'], False),
				saca_porcentajes(objeto['primaria_completa'], objeto['num_total'], False),
				saca_porcentajes(objeto['secundaria_incompleta'], objeto['num_total'], False),
				saca_porcentajes(objeto['bachiller'], objeto['num_total'], False),
				saca_porcentajes(objeto['universitario'], objeto['num_total'], False),
			]

			if e[0] in lista_hombres:
				tabla_educacion_hombre.append(fila)
			elif e[0] in lista_mujeres:
				tabla_educacion_mujer.append(fila)

	years[year] = (cantidad_miembros_hombres,grafo_educacion_hombre,cantidad_miembros_mujeres,
					grafo_educacion_mujer,tabla_educacion_hombre,tabla_educacion_mujer)

	return render(request, template, locals())

def tenencia_propiedad(request,template="productores/tenencia_propiedad.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()
	for year in request.session['year']:
		dueno = filtro.filter(tenenciapropiedad__dueno_propiedad = 1,year = year).count()

		no_dueno = filtro.filter(tenenciapropiedad__dueno_propiedad = 2,year = year).count()

		nombre_propiedad = {}
		for obj in PROPIEDAD_CHOICE:
			conteo = filtro.filter(year = year,tenenciapropiedad__si = obj[0]).count()
			nombre_propiedad[obj[1]] = conteo

		situacion_propiedad = {}
		for obj in SituacionesPropiedad.objects.all():
			conteo = filtro.filter(year = year,tenenciapropiedad__no = obj).count()
			situacion_propiedad[obj] = conteo

	years[year] = (dueno,no_dueno,nombre_propiedad,situacion_propiedad)

	return render(request, template, locals())

def uso_tierra(request,template="productores/uso_tierra.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()
	for year in request.session['year']:
		areas_finca = {}
		total_areas = filtro.filter(year = year).aggregate(
							suma = Sum('detalleareafinca__area'))['suma']

		for obj in CHOICE_TIERRA:
			area = filtro.filter(year = year,detalleareafinca__seleccion = obj[0]).aggregate(
								suma = Sum('detalleareafinca__area'))['suma']
			areas_finca[obj[1]] = (area,saca_porcentajes(area,total_areas,False))

		years[year] = areas_finca

	return render(request, template, locals())

def reforestacion(request,template="productores/reforestacion.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()
	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		reforestacion = {}
		for obj in REFORESTACION_CHOICE:
			frecuencia = filtro.filter(year = year,reforestacion__seleccion = obj[0],reforestacion__respuesta = 1).count()
			reforestacion[obj[1]] = (saca_porcentajes(frecuencia,productores,False),frecuencia)

		years[year] = reforestacion

	return render(request, template, locals())

def caracterizacion_terreno(request,template="productores/caracterizacion_terreno.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()
	for year in request.session['year']:
		productores = filtro.filter(year = year).count()

		tabla_textura = {}
		for k in TEXTURA_CHOICES:
			query = filtro.filter(year = year,caracterizacionterreno__textura_suelo = k[0])
			frecuencia = query.count()
			textura = filtro.filter(year = year,caracterizacionterreno__textura_suelo = k[0]).aggregate(
								textura = Count('caracterizacionterreno__textura_suelo'))['textura']
			por_textura = saca_porcentajes(textura, productores)
			tabla_textura[k[1]] = {'textura':textura,'por_textura':por_textura}

		#pendiente
		tabla_pendiente = {}
		for k in PENDIENTE_CHOICES:
			query = filtro.filter(year = year,caracterizacionterreno__pendiente_terreno = k[0])
			frecuencia = query.count()
			pendiente = filtro.filter(year = year,caracterizacionterreno__pendiente_terreno = k[0]).aggregate(
								pendiente = Count('caracterizacionterreno__pendiente_terreno'))['pendiente']
			por_pendiente = saca_porcentajes(pendiente, productores)
			tabla_pendiente[k[1]] = {'pendiente':pendiente,'por_pendiente':por_pendiente}

		#hojarasca
		tabla_hojarasca = {}
		for k in HOJARASCA_CHOICES:
			query = filtro.filter(year = year,caracterizacionterreno__contenido_hojarasca = k[0])
			frecuencia = query.count()
			hojarasca = filtro.filter(year = year,caracterizacionterreno__contenido_hojarasca = k[0]).aggregate(
								hojarasca=Count('caracterizacionterreno__contenido_hojarasca'))['hojarasca']
			por_hojarasca = saca_porcentajes(hojarasca, productores)
			tabla_hojarasca[k[1]] = {'hojarasca':hojarasca,'por_hojarasca':por_hojarasca}

		#profundidad
		tabla_profundidad = {}
		for k in PROFUNDIDAD_CHOICES:
			query = filtro.filter(year = year,caracterizacionterreno__porfundidad_suelo = k[0])
			frecuencia = query.count()
			profundidad = filtro.filter(year = year,caracterizacionterreno__porfundidad_suelo = k[0]).aggregate(
									profundidad=Count('caracterizacionterreno__porfundidad_suelo'))['profundidad']
			por_profundidad = saca_porcentajes(profundidad, productores)
			tabla_profundidad[k[1]] = {'profundidad':profundidad,'por_profundidad':por_profundidad}

		#drenaje
		tabla_drenaje = {}
		for k in DRENAJE_CHOICES:
			query = filtro.filter(year = year,caracterizacionterreno__drenaje_suelo = k[0])
			frecuencia = query.count()
			drenaje = filtro.filter(year = year,caracterizacionterreno__drenaje_suelo = k[0]).aggregate(
								drenaje = Count('caracterizacionterreno__drenaje_suelo'))['drenaje']
			por_drenaje = saca_porcentajes(drenaje, productores)
			tabla_drenaje[k[1]] = {'drenaje':drenaje,'por_drenaje':por_drenaje}

		years[year] = (tabla_textura,tabla_pendiente,tabla_hojarasca,tabla_profundidad,tabla_drenaje)

	return render(request, template, locals())

def riesgos_finca(request,template="productores/riesgos_finca.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		riesgos = collections.OrderedDict()
		for obj in RIESGOS_CHOICES:
			sequia = filtro.filter(year = year,fenomenosnaturales__sequia = obj[0]).count()
			innundacion = filtro.filter(year = year,fenomenosnaturales__innundacion = obj[0]).count()
			lluvia = filtro.filter(year = year,fenomenosnaturales__lluvia = obj[0]).count()
			viento = filtro.filter(year = year,fenomenosnaturales__viento = obj[0]).count()
			deslizamiento = filtro.filter(year = year,fenomenosnaturales__deslizamiento = obj[0]).count()

			riesgos[obj[1]] = (saca_porcentajes(sequia,productores,False),
								saca_porcentajes(innundacion,productores,False),
								saca_porcentajes(lluvia,productores,False),
								saca_porcentajes(viento,productores,False),
								saca_porcentajes(deslizamiento,productores,False))

		plantas_improductivas = collections.OrderedDict()
		for obj in P_IMPRODUCTIVAS_CHOICES:
			p_improduct = filtro.filter(year = year,razonesagricolas__plantas_improductivas = obj[0]).count()
			plantas_improductivas[obj[1]] = saca_porcentajes(p_improduct,productores,False)

		plagas = {}
		for obj in SI_NO_CHOICES:
			plagas_enfermedades = filtro.filter(year = year,razonesagricolas__plagas_enfermedades = obj[0]).count()
			quemas = filtro.filter(year = year,razonesagricolas__quemas = obj[0]).count()

			plagas[obj[1]] = (saca_porcentajes(plagas_enfermedades,productores,False),
								saca_porcentajes(quemas,productores,False))

		mercados = {}
		for obj in SI_NO_CHOICES:
			bajo_precio = filtro.filter(year = year,razonesmercado__bajo_precio = obj[0]).count()
			falta_venta = filtro.filter(year = year,razonesmercado__falta_venta = obj[0]).count()
			estafa_contrato = filtro.filter(year = year,razonesmercado__estafa_contrato = obj[0]).count()
			calidad_producto = filtro.filter(year = year,razonesmercado__calidad_producto = obj[0]).count()

			mercados[obj[1]] = (saca_porcentajes(bajo_precio,productores,False),
								saca_porcentajes(falta_venta,productores,False),
								saca_porcentajes(estafa_contrato,productores,False),
								saca_porcentajes(calidad_producto,productores,False))

		inversion = {}
		for obj in SI_NO_CHOICES:
			invierte_cacao = filtro.filter(year = year,inversion__invierte_cacao = obj[0]).count()
			interes_invertrir = filtro.filter(year = year,inversion__interes_invertrir = obj[0]).count()
			falta_credito = filtro.filter(year = year,inversion__falta_credito = obj[0]).count()
			altos_intereses = filtro.filter(year = year,inversion__altos_intereses = obj[0]).count()
			robo_producto = filtro.filter(year = year,inversion__robo_producto = obj[0]).count()

			inversion[obj[1]] = (saca_porcentajes(invierte_cacao,productores,False),
								saca_porcentajes(interes_invertrir,productores,False),
								saca_porcentajes(falta_credito,productores,False),
								saca_porcentajes(altos_intereses,productores,False),
								saca_porcentajes(robo_producto,productores,False))

		years[year] = (riesgos,plantas_improductivas,plagas,mercados,inversion)

	return render(request, template, locals())

def mitigacion_riesgos(request,template="productores/mitigacion_riesgos.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		mitigacion_riesgos = {}
		contrato_venta = {}
		tecnologia = {}

		for k in SI_NO_CHOICES:
			monitoreo_plagas = filtro.filter(year = year,mitigacionriesgos__monitoreo_plagas = k[0]).count()
			manejo_cultivo = filtro.filter(year = year,mitigacionriesgos__manejo_cultivo = k[0]).count()
			manejo_recursos = filtro.filter(year = year,mitigacionriesgos__manejo_recursos = k[0]).count()
			almacenamiento_agua = filtro.filter(year = year,mitigacionriesgos__almacenamiento_agua = k[0]).count()
			distribucion_cacao = filtro.filter(year = year,mitigacionriesgos__distribucion_cacao = k[0]).count()

			mitigacion_riesgos[k[1]] = (monitoreo_plagas,manejo_cultivo,manejo_recursos,
											almacenamiento_agua,distribucion_cacao)

			#contrato venta
			venta_cacao = filtro.filter(year = year,mitigacionriesgos__venta_cacao = k[0]).count()
			contrato_venta[k[1]] = venta_cacao

			#tecnologia de secado
			tecnologia_secado = filtro.filter(year = year,mitigacionriesgos__tecnologia_secado = k[0]).count()
			tecnologia[k[1]] = tecnologia_secado

		#como hacen el contrato
		contrato = {}
		for obj in VENTA_CHOICES:
			conteo = filtro.filter(year = year,mitigacionriesgos__si_venta_cacao = obj[0]).count()
			contrato[obj[1]] = conteo

		#tecnologia d secado: propia/Cooperativa
		propiedad_tecnologia = {}
		for obj in TECNOLOGIA_CHOICES:
			conteo = filtro.filter(year = year,mitigacionriesgos__si_tecnologia_secado = obj[0]).count()
			propiedad_tecnologia[obj[1]] = conteo

		years[year] = (mitigacion_riesgos,productores,contrato_venta,contrato,tecnologia,propiedad_tecnologia)

	return render(request, template, locals())

def organizacion_productiva(request,template="productores/organizacion_productiva.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		servicios = {}
		beneficios = {}
		for obj in TiposServicio.objects.all():
			conteo = filtro.filter(year = year,serviciosorganizado__tipos_servicio = obj).count()
			servicios[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		for obj in Beneficios.objects.all():
			conteo = filtro.filter(year = year,beneficiosorganizado__beneficios = obj).count()
			beneficios[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		years[year] = (servicios,beneficios)

	return render(request, template, locals())

def produccion(request,template="productores/produccion.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	EDAD_PLANTA_CHOICES = (
		(3,'De 4 a 10 años'),
		(4,'De 10 a 20 años'),
		(5,'Mayores de 20 años'),
	)

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		edades = collections.OrderedDict()
		for obj in EDAD_PLANTA_CHOICES:
			area_total = filtro.filter(year = year,plantacion__edad = obj[0]).aggregate(
											total = Sum('plantacion__area'))['total']
			#----------------------------------------------------------------------------------------------------
			numero_plantas = filtro.filter(year = year,plantacion__edad = obj[0]).aggregate(
											plantas=Sum('plantacion__numero_plantas'))['plantas']
			try:
				numero_plantas = numero_plantas / area_total
			except:
				numero_plantas = 0
			#----------------------------------------------------------------------------------------------------
			improductivas = filtro.filter(year = year,plantacion__edad = obj[0]).aggregate(
											improductivas = Sum('plantacion__plantas_improductivas'))['improductivas']

			plant_improd = saca_porcentajes(improductivas,numero_plantas,False)
			#----------------------------------------------------------------------------------------------------
			semillas = filtro.filter(year = year,plantacion__edad = obj[0]).aggregate(
											semillas = Sum('plantacion__plantas_semilla'))['semillas']

			plantas_semillas = saca_porcentajes(semillas,numero_plantas,False)
			#----------------------------------------------------------------------------------------------------
			injerto = filtro.filter(year = year,plantacion__edad = obj[0]).aggregate(
											injerto = Sum('plantacion__plantas_injerto'))['injerto']

			plantas_injerto = saca_porcentajes(injerto,numero_plantas,False)
			#----------------------------------------------------------------------------------------------------

			edades[obj[1]] = (area_total, numero_plantas, plant_improd, plantas_semillas, plantas_injerto)

		#produccion cacao
		convencional = filtro.filter(year = year,certificacion__cacao_certificado = '2').aggregate(
											convencional=Sum('produccioncacao__cacao_baba'))['convencional']
		if convencional == None:
			convencional = 0

		fermentado = filtro.filter(year = year,certificacion__cacao_certificado = '1').aggregate(
											fermentado=Sum('produccioncacao__cacao_baba'))['fermentado']
		if fermentado == None:
			fermentado = 0

		#meses de produccion
		meses_prod = collections.OrderedDict()
		for obj in MESES_CHOICES:
			frecuencia = filtro.filter(year = year,produccioncacao__meses__icontains = obj[0]).count()
			meses_prod[obj[1]] = frecuencia

		years[year] = (edades,convencional,fermentado,meses_prod)

	return render(request, template, locals())

def certificacion(request,template="productores/certificacion.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		#certificaciones
		certificaciones = {}
		for obj in CERTIFICACIONES_CHOICES:
			conteo = filtro.filter(year = year, certificacion__tipo__icontains = obj[0]).count()
			certificaciones[obj[1]] = conteo

		#productores certificados y no certificados
		certificados = filtro.filter(year = year,certificacion__cacao_certificado = 1).count()
		no_certificados = filtro.filter(year = year,certificacion__cacao_certificado = 2).count()

		# #No de productores con uno o más sellos
		x = 0
		y = 0
		z = 0
		lista_certificaciones = []
		for obj in filtro.filter(year = year):
			num_certif = 0
			for cert in Certificacion.objects.filter(cacao_certificado = 1,encuesta = obj):
				for tipo in cert.tipo:
					num_certif += 1
			if num_certif == 1:
				x += 1
			elif num_certif == 2:
				y += 1
			elif num_certif > 2:
				z += 1
		lista_certificaciones.append([x, y, z])

		quien_certifica = {}
		for obj in QuienCertifica.objects.all():
			conteo = filtro.filter(year = year,certificacion__quien_certifica = obj).count()
			quien_certifica[obj] = conteo

		quien_paga= {}
		for obj in PAGA_CERT_CHOICES:
			conteo = filtro.filter(year = year,certificacion__paga_certificacion = obj[0]).count()
			quien_paga[obj[1]] = conteo

		mantenimiento_cacao = filtro.filter(year = year).aggregate(costo = Avg('costoproduccion__mantenimiento_cacao'))
		mantenimiento_finca = filtro.filter(year = year).aggregate(costo = Avg('costoproduccion__mantenimiento_finca'))

		years[year] = (productores,certificaciones,certificados,no_certificados,lista_certificaciones,
						quien_certifica,quien_paga,mantenimiento_cacao,mantenimiento_finca)

	return render(request, template, locals())

def tecnicas_aplicadas(request,template="productores/tecnicas_aplicadas.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		#viveros
		viveros = {}
		for obj in VIVEROS_CHOICES:
			conteo = filtro.filter(year = year,tecnicasaplicadas__viveros__icontains = obj[0]).count()
			viveros[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		#fertilizacion
		fertilizacion = {}
		for obj in FERTILIZACION_CHOICES:
			conteo = filtro.filter(year = year,tecnicasaplicadas__fertilizacion__icontains = obj[0]).count()
			fertilizacion[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		#manejo_fis
		manejo_fis = {}
		for obj in MANEJO_FIS_CHOICES:
			conteo = filtro.filter(year = year,tecnicasaplicadas__pract_manejo_fis__icontains = obj[0]).count()
			manejo_fis[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		#manejo_prod
		manejo_prod = {}
		for obj in MANEJO_PROD_CHOICES:
			conteo = filtro.filter(year = year,tecnicasaplicadas__pract_manejo_prod__icontains = obj[0]).count()
			manejo_prod[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		#mejora_plat
		mejora_plat = {}
		for obj in MEJORA_PLANTACION_CHOICES:
			conteo = filtro.filter(year = year,tecnicasaplicadas__pract_mejora_plat__icontains = obj[0]).count()
			mejora_plat[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		#manejo_post
		manejo_post = {}
		for obj in MANEJO_POSTCOSECHA_CHOICES:
			conteo = filtro.filter(year = year,tecnicasaplicadas__pract_manejo_post_c__icontains = obj[0]).count()
			manejo_post[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		acopio_cacao = {}
		acopio_org = {}
		for obj in SI_NO_CHOICES:
			cacao = filtro.filter(year = year,tecnicasaplicadas__acopio_cacao = obj[0]).count()
			acopio_cacao[obj[1]] = cacao

			org = filtro.filter(year = year,tecnicasaplicadas__acopio_org = obj[0]).count()
			acopio_org[obj[1]] = org

		years[year] = (viveros,fertilizacion,manejo_fis,manejo_prod,mejora_plat,manejo_post,
						acopio_cacao,acopio_org)

	return render(request, template, locals())

def comercializacion(request,template="productores/comercializacion.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()

		#tabla comercio
		comercio = []
		for obj in PRODUCTO_CHOICES:
			producto = filtro.filter(year = year,comercializacioncacao__producto = obj[0]).aggregate(
					auto_consumo = Sum('comercializacioncacao__auto_consumo'),
					venta = Sum('comercializacioncacao__venta'),
					precio_venta = Avg('comercializacioncacao__precio_venta'))

			lista = []
			for x in QUIEN_VENDE_CHOICES:
				conteo = filtro.filter(year = year,comercializacioncacao__producto = obj[0],
										comercializacioncacao__quien_vende__icontains = x[0]).count()
				lista.append(saca_porcentajes(conteo,productores,False))

			comercio.append(
						(obj[1],
						producto['auto_consumo'],producto['venta'],
						producto['precio_venta'],lista[0],lista[1],
						lista[2],lista[3]
						))

		#distancia recorrida avg
		distancia = filtro.filter(year = year).aggregate(avg = Avg('distanciacomerciocacao__distancia'))['avg']

		#grafico venta
		PRODUCTOS = (
			(3,'Cacao en baba (qq)'),
			(4,'Cacao rojo sin fermentar (qq)'),
			(5,'Cacao fermentado (qq)'),
			)

		venta = {}
		for obj in PRODUCTOS:
			qq = filtro.filter(year = year,comercializacioncacao__producto = obj[0]).aggregate(
											total = Sum('comercializacioncacao__venta'))['total']
			if qq == None:
				qq = 0
			venta[obj[1]] = qq

		years[year] = (distancia,comercio,venta)

	return render(request, template, locals())

def capacitaciones(request,template="productores/capacitaciones.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		#capacitaciones tecnicas
		tecnicas = {}
		for obj in CAPACITACIONES_CHOICES:
			lista_tec = []
			total = 0
			for x in OPCIONES_CAPACITACIONES_CHOICES:
				conteo = filtro.filter(year = year,capacitacionestecnicas__capacitaciones = obj[0],
										capacitacionestecnicas__opciones__icontains = x[0]).count()
				lista_tec.append(conteo)
			tecnicas[obj[1]] = lista_tec

		#grafico tecnicas
		graf_tecnicas = {}
		for obj in OPCIONES_CAPACITACIONES_CHOICES:
			conteo = filtro.filter(year = year,capacitacionestecnicas__opciones__icontains = obj[0]).count()
			graf_tecnicas[obj[1]] = conteo

		#capacitaciones socio
		socio = {}
		for obj in CAPACITACIONES_SOCIO_CHOICES:
			lista_socio = []
			total = 0
			for x in OPCIONES_CAPACITACIONES_CHOICES:
				conteo = filtro.filter(year = year,capacitacionessocioeconomicas__capacitaciones_socio = obj[0],
										capacitacionessocioeconomicas__opciones_socio__icontains = x[0]).count()
				lista_socio.append(conteo)
			socio[obj[1]] = lista_socio

		#grafico socio
		graf_socio = {}
		for obj in OPCIONES_CAPACITACIONES_CHOICES:
			conteo = filtro.filter(year = year,capacitacionessocioeconomicas__opciones_socio__icontains = obj[0]).count()
			graf_socio[obj[1]] = conteo

		years[year] = (graf_tecnicas,tecnicas,graf_socio,socio)

	return render(request, template, locals())

def problemas_areas_cacao(request,template="productores/problemas_cacao.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		area_1 = {}
		for obj in ProblemasArea1.objects.all():
			conteo = filtro.filter(year = year,problemasareacacao__area_1 = obj).count()
			area_1[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		area_2 = {}
		for obj in ProblemasArea2.objects.all():
			conteo = filtro.filter(year = year,problemasareacacao__area_2 = obj).count()
			area_2[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		area_3 = {}
		for obj in ProblemasArea3.objects.all():
			conteo = filtro.filter(year = year,problemasareacacao__area_3 = obj).count()
			area_3[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		years[year] = (area_1,area_2,area_3)

	return render(request, template, locals())

def genero(request,template="productores/genero.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()

		#participacion
		participacion = {}
		for obj in ActividadesProduccion.objects.all():
			conteo = filtro.filter(year = year,genero__actividades = obj).count()
			participacion[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		#decisiones
		DECISIONES_CHOICES = (
			(1,'Siembra'),
			(2,'Cosecha'),
			(3,'Venta'),
			(4,'Uso de los ingresos'),
			)
		decisiones = {}
		for obj in DECISIONES_CHOICES:
			conteo = filtro.filter(year = year,genero__decisiones__icontains = obj[0]).count()
			decisiones[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		#otros_ingresos
		otros_ingresos = {}
		for obj in OtrosIngresos.objects.all():
			conteo = filtro.filter(year = year,genero__otros_ingresos = obj).count()
			otros_ingresos[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		#ingresos
		ingresos = {}
		for obj in SI_NO_CHOICES:
			conteo = filtro.filter(year = year,genero__ingresos = obj[0]).count()
			ingresos[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		#avg ingresos
		ingreso_mesual_cacao = filtro.filter(year = year).aggregate(avg = Avg('genero__ingreso_mesual_cacao'))['avg']
		ingreso_mesual = filtro.filter(year = year).aggregate(avg = Avg('genero__ingreso_mesual'))['avg']

		#destino ingresos
		destino_ingresos = {}
		for obj in DestinoIngresos.objects.all():
			conteo = filtro.filter(year = year,genero__destino_ingresos = obj).count()
			destino_ingresos[obj] = (conteo,saca_porcentajes(conteo,productores,False))

		years[year] = (participacion,decisiones,otros_ingresos,ingresos,ingreso_mesual_cacao,ingreso_mesual,destino_ingresos)

	return render(request, template, locals())

def ampliar_areas_cacao(request,template="productores/ampliar_areas.html"):
	filtro = _queryset_filtrado(request)

	years = collections.OrderedDict()

	for year in request.session['year']:
		productores = filtro.filter(year = year).count()
		interes = {}
		for obj in SI_NO_CHOICES:
			conteo = filtro.filter(year = year,ampliarareascacao__interes = obj[0]).count()
			interes[obj[1]] = (conteo,saca_porcentajes(conteo,productores,False))

		total_areas = filtro.filter(year = year).aggregate(total = Sum('ampliarareascacao__cuanto'))['total']
		promedio_areas = filtro.filter(year = year).aggregate(total = Avg('ampliarareascacao__cuanto'))['total']

		years[year] = (interes,total_areas,promedio_areas)

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
				encuesta = Encuesta.objects.filter(entrevistado__municipio__departamento__id = id).distinct().values_list('entrevistado__municipio__id', flat=True)
				departamento = Departamento.objects.get(pk=id)
				municipios = Municipio.objects.filter(departamento__id=departamento.pk,id__in = encuesta).order_by('nombre')
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
