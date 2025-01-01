from django.shortcuts import render
from .models import *
import sqlite3


def index(request):
    template = 'main/index.html'
    context = {}
    return render(request, template, context)