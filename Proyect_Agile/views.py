from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render

def iniciosesion(request):


    return HttpResponse(render(request,"Proyect_Agile/iniciosesion.html"))
