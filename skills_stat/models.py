from django.db import models

class Skill_filtered(models.Model):
    name = models.CharField("Навык", max_length = 64)
    count = models.IntegerField("Кол-во упоминаний")

    class Meta:
        db_table = "skills_filtered"