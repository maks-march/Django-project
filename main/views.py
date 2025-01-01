from django.shortcuts import render
from .models import City

def index(request):
    data = City.objects.all()
    template = 'main/index.html'
    context = {'cities': data}
    return render(request, template, context)