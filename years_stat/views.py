from django.shortcuts import render

from years_stat.models import Year_filtered

def popularity(request):
    data_year = Year_filtered.objects.all()
    template = 'years_stat/popularity.html'
    context = {'year': data_year}
    return render(request, template, context)