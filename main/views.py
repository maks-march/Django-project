from django.shortcuts import render
from .models import City

def index(request):
    template = 'main/index.html'
    return render(request, template)

def all(request):
    data = City.objects.all()
    template = 'main/all.html'
    context = {'cities': data}
    return render(request, template)