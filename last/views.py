from django.shortcuts import render

def last(request):
    template = 'last/last.html'
    context = {}
    return render(request, template, context)