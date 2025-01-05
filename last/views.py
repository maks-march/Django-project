from django.shortcuts import render
import requests, locale
from datetime import datetime, timedelta

def last(request):
    template = 'last/last.html'
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"  # Note: do not use "de_DE" as it doesn't work
    )
    BASE_DIR = 'https://api.hh.ru/vacancies'
    date_from = (datetime.now() - timedelta(days=1)).isoformat()
    profession = '(NAME:разработчик OR NAME:программист OR NAME:инженер) AND NAME:C++ AND NOT 1C'
    url = f'{BASE_DIR}?date_from={date_from}&text={profession}&per_page=10';

    response = requests.get(url)
    data = response.json()
    vacancies = data.get('items', [])
    data = []
    for vacancy in vacancies:
        new_vac = {}
        new_vac['name'] = vacancy['name']
        url = vacancy['url']
        response = requests.get(url)
        vac_data = response.json()
        new_vac['description'] = vac_data['description']
        skills = ", ".join(skill['name'] for skill in vac_data['key_skills'])
        new_vac['skills'] = skills
        new_vac['employer'] = vacancy['employer']['name']
        if vacancy['salary'] == None:
            new_vac['salary'] = ''
        else:
            salary = ''
            if vacancy['salary']['from'] != None:
                salary = salary + f"от {vacancy['salary']['from']} "
            if vacancy['salary']['to'] != None:
                salary = salary + f"до {vacancy['salary']['to']} "
            new_vac['salary'] = salary + "рублей"
        new_vac['area_name'] = vacancy['area']['name']
        new_vac['published_at'] = datetime.strptime(vacancy['published_at'][:-5], "%Y-%m-%dT%H:%M:%S").strftime("%A, %d %B %Y, %H:%M:%S")
        data.append(new_vac)
    context = {'vacancies': data}
    return render(request, template, context)