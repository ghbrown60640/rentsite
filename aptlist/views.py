from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the aptlist index.")


def detail(request, apartment_id):
    return HttpResponse("You're looking at apartment %s." % apartment_id)


def results(request, apartment_id):
    response = "You're looking at the results of apartment %s."
    return HttpResponse(response % apartment_id)


def vote(request, apartment_id):
    return HttpResponse("You're voting on apartment %s." % apartment_id)
