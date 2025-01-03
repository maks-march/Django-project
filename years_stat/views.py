from django.shortcuts import render

def popularity(request):
    template = 'years_stat/popularity.html'
    context = {}
    return render(request, template, context)