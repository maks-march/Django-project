from django.shortcuts import render

from skills_stat.models import Skill_filtered


def skills(request):
    data_skills = Skill_filtered.objects.all()
    template = 'skills_stat/skills.html'
    context = {'skills': data_skills}
    return render(request, template, context)