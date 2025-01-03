from django.shortcuts import render
from .models import City, Skill, Year

def index(request):
    template = 'main/index.html'
    return render(request, template)

def all(request):
    data_city = City.objects.all()
    data_skills = Skill.objects.all()
    data_years = Year.objects.all()
    template = 'main/all.html'
    context = {'cities': data_city, 'skills': data_skills, 'years': data_years}
    return render(request, template, context)