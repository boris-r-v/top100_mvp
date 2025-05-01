from django.db import models

class Excursion(models.Model):
    city = models.CharField(max_length=100, verbose_name="Город")
    company = models.CharField(max_length=100, verbose_name="Предприятие")
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.company} ({self.city})"    