from django.shortcuts import render
from .models import City, Skill, Year

def index(request):
    template = 'main/index.html'
    return render(request, template)

def all(request):
    data_city = City.objects.all().filter(proportion__gte = 1).order_by("-proportion")
    data_skills = Skill.objects.all().filter(count__gte = 10000).order_by("-count")
    data_years = Year.objects.all().order_by("-year")
    template = 'main/all.html'
    context = {'cities': data_city, 'skills': data_skills, 'years': data_years}
    return render(request, template, context)