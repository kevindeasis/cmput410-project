from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render


def index(request):
    return render(request, 'LandingPage/index.html', None)
#    return HttpResponse("Hello, world. You're at the  index.")
