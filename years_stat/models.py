from django.db import models

class Year_filtered(models.Model):
    year = models.CharField("Год", max_length = 64)
    average_salary = models.FloatField("Средняя зарплата")
    count = models.FloatField("Кол-во вакансий")

    class Meta:
        db_table = "years_filtered"