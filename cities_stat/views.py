from django.shortcuts import render
from cities_stat.models import City_filtered

def geography(request):
    data_city = City_filtered.objects.all()
    template = 'cities_stat/geography.html'
    context = {'cities': data_city}
    return render(request, template, context)