from django.shortcuts import render, HttpResponse
from django.template import loader


def index(request):

    template = loader.get_template('home.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello, world. You're at the create_event index.")




