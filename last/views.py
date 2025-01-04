from django.shortcuts import render
import requests
from datetime import datetime, timedelta



def last(request):
    template = 'last/last.html'

    BASE_DIR = 'https://api.hh.ru/vacancies'
    date_from = (datetime.now() - timedelta(days=1)).isoformat()
    profession = 'C++'
    url = f"{BASE_DIR}?date_from={date_from}&text=${profession}&per_page=10&order_by=published_at";

    headers = {
        'Authorization': 'Bearer HH-User-Agent'  # Замените на ваш токен
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    vacancies = data.get('items', [])
    context = {'vacancies': vacancies, 'response': response.status_code}
    return render(request, template, context)