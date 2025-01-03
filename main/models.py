from django.db import models

# Использовалась при анализе vacancies.csv
# class Vacancy(models.Model):
#     id = models.IntegerField("id", primary_key = True)
#     name = models.CharField("Название", max_length = 64)
#     key_skills = models.CharField("Ключевые навыки", max_length = 512, blank = True, null = True)
#     salary_from = models.FloatField("Зарплата от")
#     salary_to = models.FloatField("Зарплата до")
#     salary_average = models.FloatField("Средняя зарплата")
#     salary_currency = models.CharField("Валюта", max_length = 64, blank = True, null = True)
#     area_name = models.CharField("Местоположение", max_length = 64, blank = True, null = True)
#     published_at = models.DateTimeField("Время публикации", null = True)
#     date = models.IntegerField("Год публикации", null = True)
#
#     class Meta:
#         db_table = "vacancies"


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
    count = models.FloatField("Кол-во вакансий")

    class Meta:
        db_table = "years"

