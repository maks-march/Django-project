from django.db import models

class Vacancy(models.Model):
    name = models.CharField("Название")
    key_skills = models.CharField("Ключевые навыки")
    salary_from = models.FloatField("Зарплата от")
    salary_to = models.FloatField("Зарплата до")
    salary_average = models.FloatField("Средняя зарплата")
    salary_currency = models.CharField("Валюта")
    area_name = models.CharField("Местоположение")
    published_at = models.DateTimeField("Время публикации")

    class Meta:
        db_table = "vacancies"

class Skill(models.Model):
    name = models.CharField("Навык")
    count = models.IntegerField("Кол-во упоминаний")

    class Meta:
        db_table = "skills"

class City(models.Model):
    name = models.CharField("Название")
    average_salary = models.FloatField("Средняя зарплата")
    proportion = models.FloatField("Доля вакансий")

    class Meta:
        db_table = "cities"

class Year(models.Model):
    year = models.CharField("Год")
    average_salary = models.FloatField("Средняя зарплата")
    proportion = models.FloatField("Кол-во вакансий")

    class Meta:
        db_table = "years"