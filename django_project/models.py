from django.db import models

class Vacancy(models.Model):
    name = models.CharField("Название", max_length = 64)
    key_skills = models.CharField("Ключевые навыки", max_length = 512)
    salary_from = models.FloatField("Зарплата от")
    salary_to = models.FloatField("Зарплата до")
    salary_average = models.FloatField("Средняя зарплата")
    salary_currency = models.CharField("Валюта", max_length = 64)
    area_name = models.CharField("Местоположение", max_length = 64)
    published_at = models.DateTimeField("Время публикации")

    class Meta:
        db_table = "vacancies"

class Skill(models.Model):
    name = models.CharField("Навык", max_length = 64)
    count = models.IntegerField("Кол-во упоминаний")

    class Meta:
        db_table = "skills"

class City(models.Model):
    name = models.CharField("Название", max_length = 64)
    average_salary = models.FloatField("Средняя зарплата")
    proportion = models.FloatField("Доля вакансий")

    class Meta:
        db_table = "cities"

class Year(models.Model):
    year = models.CharField("Год", max_length = 64)
    average_salary = models.FloatField("Средняя зарплата")
    proportion = models.FloatField("Кол-во вакансий")

    class Meta:
        db_table = "years"