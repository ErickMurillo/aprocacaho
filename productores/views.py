from django.shortcuts import render

# Create your views here.
def consulta_productores(request,template="productores/consulta.html"):

    return render(request, template, locals())
