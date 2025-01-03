from django.shortcuts import render

def geography(request):
    template = 'cities_stat/geography.html'
    context = {}
    return render(request, template, context)