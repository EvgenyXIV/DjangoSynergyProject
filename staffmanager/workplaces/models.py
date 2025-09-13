from django.db import models

# Create your models here.


class Workplace(models.Model):
    table = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"

    def __str__(self):
        if self.table:
            return f"Рабочее место №{self.table}"
        else:
            return "Рабочее место не назначено"
