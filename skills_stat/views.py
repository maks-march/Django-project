from django.shortcuts import render

def skills(request):
    template = 'skills_stat/skills.html'
    context = {}
    return render(request, template, context)