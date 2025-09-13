from django.contrib import admin
from .models import Workplace
from staff.models import Employee

# Register your models here.


# Назначаем рабочие места прямо в фоме сотрудника
class EmployeeInline(admin.StackedInline):
    model = Employee
    extra = 0


# Добавляем форму для ввода рабочих мест в админку в форме сотрудника
inlines = [EmployeeInline]
admin.site.register(
    Workplace,
)
