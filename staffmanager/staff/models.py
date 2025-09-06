from django.db import models
from django.contrib.auth.models import User  # Импортируем модель User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)  # Для валидации поля level
from workplaces.models import Workplace  # Импортируем модель Workplace
from django_ckeditor_5.fields import (
    CKEditor5Field,
)  # Импортируем класс поля WYSIWYG-редактора django-ckeditor-5


# Create your models here.


class Skill(models.Model):  # Класс Навык наследник базовой модели Model
    name = models.CharField(max_length=100)
    # Поле описания навыка (по желанию)
    description = CKEditor5Field(blank=True, null=True)

    # Добавляем читабельность в админке
    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Employee(models.Model):  # Класс Сотрудник наследник базовой модели Model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Связь с моделью User один к одному
    # Выбор пола
    gender = models.CharField(
        max_length=10, choices=(("male", "Мужской"), ("female", "Женский"))
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    # Отчество (по желанию)
    middle_name = models.CharField(
        max_length=100, verbose_name="Отчество", blank=True, null=True
    )
    # Связь с моделью Skill многие ко многим через модель SkillLevel
    skills = models.ManyToManyField(Skill, through="SkillLevel")
    # Связь с моделью Workplace один к одному.
    # Если не назначено, то в карточке сотрудника будет отображаться 'Рабочее место не назначено'
    # Удаление рабочего места не привидёт к удалению сотрудника (on_delete=models.SET_NULL)
    workplace = models.OneToOneField(
        Workplace,
        on_delete=models.SET_NULL,
        verbose_name="Рабочее место",
        blank=True,
        null=True,
    )
    # Описание сотрудника (по желанию)
    description = CKEditor5Field(blank=True, null=True)

    # Добавляем читабельность в админке
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    # В заголовке карточки сотрудника вместо Employee object() будет имя и фамилия
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Связь сотрудник/навык многие ко многим через модель SkillLevel
class SkillLevel(models.Model):  # Класс Уровень Навыка наследник базовой модели Model
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:  # Добавляем читабельность в админке
        verbose_name = "Уровень навыка"
        verbose_name_plural = "Уровни навыка"

    # Выводим в админке в виде: 'Сотрудник - Навык (уровень 1)'.
    # Если уровень 1, то выводим только 'Сотрудник - Навык'
    def __str__(self):
        if self.level == 1:
            return f"{self.employee} - {self.skill}"
        else:
            return f"{self.employee} - {self.skill} (уровень {self.level})"
