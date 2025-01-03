from django.db import models


class City_filtered(models.Model):
    name = models.CharField("Название", max_length = 64)
    average_salary = models.FloatField("Средняя зарплата")
    proportion = models.FloatField("Доля вакансий")

    class Meta:
        db_table = "cities_filtered"