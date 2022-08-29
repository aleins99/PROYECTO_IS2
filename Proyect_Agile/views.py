from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render
from django.urls import reverse
def iniciosesion(request):
    login = reverse('account_login')
    return HttpResponseRedirect(login)
