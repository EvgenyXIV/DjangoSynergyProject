# DJANGO

**ДЗ 1**
__Создано виртуальное окружение python 3.12 в папке DjangoSynergyProject.venv__

python3.12 -m venv .venv
.venv/Scripts/activate

__Установка Джанго версии 5.2.1.__
py -m pip install Django==5.2.1

__Установка автоформаттера black и сортировщика импортов isort__
pip install black
python -m pip install isort

__Создание Джанго-проекта staffmanager__
django-admin startproject staffmanager

__Создание Джанго-приложений staff (хранение инф. о персонале) и workplaces (хранение инф. о рабочих сестах)__
cd  staffmanager
py manage.py startapp staff
py manage.py startapp workplaces

__Регистрация приложений в settings.py__
Application definition
INSTALLED_APPS = [
    # Регистрируем приложения учёта персонала и рабочих мест в наcтройках
    'staff',
    'workplaces',
.............

__Создание пробного обработчика запросов в файле staff/views__
"""Для простоты вместо html шаблона используем класс HttpResponse - из пакета позволяет отправить текстовое содержимое.
Функция-обработчик index() принимает запрос request и возвращает ответ 'Здесь будет главная страница'  в теге h1 - заголовок первого уровня.
Для вызова этой функции-обработчика надо в Джанго-проекте staffmanager в urls.py внести в список адресов urlpatterns
адрес path('',views.index), по которому она находится. 
Путь 'staffmanager.urls' к файлу с адресами urls.py содержится в переменной ROOT_URLCONF в настройках проекта staffmanager в файле settings.py """

from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Здесь будет главная страница<h1>")

__Внесение в список адресов обработчиков запросов в файле urls.py__
 #импортируем модуль views из папки staff, содержащую функции-обработчики запросов
from staff import views
urlpatterns = [
    path('admin/', admin.site.urls),                  # URL для обработчика из модуля 
    path('',views.index)                              # URL для обработчика index() 
]

__Запуск сервера на локальном хосте 127.0.0.1:8000__
cd staffmanager
py manage.py runserver

__Установка модуля отладки DebugToolbar__
cd..
pip install django-debug-toolbar

__Регистрация модуля отладки DebugToolbar в settings.py__
#1. Добавляем константу для DjDT, чтобы он понимал - запросы с каких IP адресов надо обрабатывать 
INTERNAL_IPS = ['127.0.0.1',]

INSTALLED_APPS = [
    ........................
    'django.contrib.staticfiles',
    # 2. Добавляем DjDT в список установленных приложений. DjDT must be after 'django.contrib.staticfiles'
    'debug_toolbar', 
]
MIDDLEWARE = [
    ...............................
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 3. Добавляем DjDT в слой Middleware в качестве middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware', 
]
__Внесение обработчика из модуля DjDT в список адресов обработчиков запросов в файле urls.py__
 #импорт модуля debug_toolbar
import debug_toolbar

 #Список всех адресов обработчиков запросов
urlpatterns = [
    path('admin/', admin.site.urls),                  # URL для обработчика из модуля 
    path('__debug__/', include(debug_toolbar.urls) ), # URL для обработчика из другого джанго-проекта    
    path('',views.index)                              # URL для обработчика index() 
]

__Сохранение зависимостей в файле requirements.txt__
pip freeze > requirements.txt

__ДЗ 2__

__Создаём суперпользователя :__
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> py manage.py createsuperuser
Имя пользователя (leave blank to use 'evgenymini_s'): user1
Адрес электронной почты: 
Password: user1
Password (again):user1
Введённый пароль слишком похож на имя пользователя.
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully

__Устанавливаем WYSIWYG-редактор django_ckeditor_5__
pip install django-ckeditor-5

in file "staffmanager\staffmanager\settings.py":
INSTALLED_APPS = [
   .......
    # Регистрация WYSIWYG-редактора django-ckeditor-5
    'django_ckeditor_5',

  #Определим конфигурацию django-ckeditor-5: включаем режим полного набора инструментов и настраиваем высоту редактора
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    }
}

in file "staffmanager\staffmanager\urls.py":
path('admin/', include('django_ckeditor_5.urls')), # URL для редактора django-ckeditor-5

in file "staffmanager\staff\models.py":
from django_ckeditor_5.fields import CKEditor5Field  # Импортируем класс поля WYSIWYG-редактора django-ckeditor-5

class Employee(models.Model):
    ...
    description = CKEditor5Field(blank=True, null=True)

__Создание модели для хранения информации о сотрудниках. Расширение встроенной модели User__
в файле staffmanager\workplaces\models.py:
from django.contrib.auth.models import User          # Импортируем модель User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Связь с моделью User один к одному
    # Выбор пола
    gender = models.CharField(max_length=10, choices=(('male', 'Мужской'), ('female', 'Женский')))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Отчество можно не указывать
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    # Связь с моделью Skills многие ко многим
    #skills = models.ManyToManyField(Skill, through='SkillLevel')         
    description = CKEditor5Field(blank=True, null=True)

    class Meta:         # Добавляем читабельность в админке
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):          # В заголовке карточки сотрудника вместо Employee object() будет имя и фамилия
        return(f'{self.first_name} {self.last_name}')


    
__Русификация полей:__
В моделях таблиц models.py и в конфигурациях  приложений apps.py указываем читабельные имена полей

В моделях models.py
 #staffmanager\staff\models.py
class Employee(models.Model):
................................
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

 #staffmanager\workplaces\models.py
 ...............................
 class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'

В конфигурациях приложений
 #staffmanager\staff\apps.py:
class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff'
    verbose_name = 'СОТРУДНИКИ'

 #staffmanager\workplaces\apps.py:
class WorkplacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workplaces'
    verbose_name = 'РАБОЧИЕ МЕСТА'

**ДЗ 2**
В приложении «сотрудники» созданы  модели для хранения
информации о сотрудниках с расширением встроенного класса User -
при создании класса Emplyee было создано отношение один-к-одному с User.
Названия полей русифицированы.
В админке "сотрудники" можно менять все поля, кроме Навыков.
Это из-за отношения многие (Сотрудники)-ко-многим(Навыки) через промежуточную таблицу Уровень навыка.
Для уровня навыка использованы валидаторы минимального(1) и максимального(10) значения уровня.
Для вывода навыков у пользователя была создана функция def employee_skills(self, obj):
Навык можно задавать в админке самого сотрудника. Для этого был наследован класс inline.
Для каждого навыка приведено описание.
Рабоичие места (один-к-одному с Сотрудниками) можно задавать как в админке сотрудника,
так и в общей админики Сотрудники.

Обновлены зависимости в файле requirements.txt:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject> pip freeze > requirements.txt

Рабочие файлы были отформатированы форматтером black:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> black staff\\
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staff\admin.py

All done! ✨ 🍰 ✨
1 file reformatted, 16 files left unchanged.
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> black staffmanager\\
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\asgi.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\wsgi.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\settings.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\urls.py

All done! ✨ 🍰 ✨
4 files reformatted, 1 file left unchanged.

(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> black workplaces\\
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\workplaces\models.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\workplaces\apps.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\workplaces\admin.py

All done! ✨ 🍰 ✨
3 files reformatted, 7 files left unchanged.

Далее приведены коды некоторых рабочих файлов:

__staffmanager\staff\models.py__

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
   

__staffmanager\staff\admin.py__

from django.contrib import admin
from .models import Employee, Skill, SkillLevel

    # Register your models here.


@admin.register(Skill)  # Регистрируем модель Skill в админке
class SkillAdmin(admin.ModelAdmin):
    model = Skill


@admin.register(SkillLevel)  # Регистрируем модель SkillLevel в админке
class SkillLevelAdmin(admin.ModelAdmin):
    model = SkillLevel


    # Inline class для таблицы SkillLevel
    # Используется класс TabularInline, который представляет собой
    # табличное представление записей в административной панели
class SkillLevelInline(admin.TabularInline):
    model = SkillLevel
    extra = 0


@admin.register(Employee)  # Регистрируем модель Employee в админке c инлайнами
class EmployeeAdmin(admin.ModelAdmin):

    # Вывод всех навыков сотрудника в админке Сотрудники
    def employee_skills(self, obj):
        # Получение всех навыков пользователя
        a = obj.skills.all().values_list("name", flat=True).distinct()
        # Получение всех уровней навыков пользователя
        b = obj.skilllevel_set.all().values_list("level", flat=True).distinct()
        # Создание списка с названиями навыков и их уровнями
        c = []
        for i in range(len(b)):
            c.append(a[i] + f"({str(b[i])})")
        # Вывод элементов списка через запятую
        return ", ".join(c)

    employee_skills.short_description = "Навыки(уровень)"

    list_display = (
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "employee_skills",
        "workplace",
        "description",
    )
    list_editable = (
        "first_name",
        "middle_name",
        "last_name",
        "workplace",
        "description",
    )
    search_fields = ("last_name",)
    list_filter = ("skills",)
    list_display_links = ("id",)
    # filter_horizontal = ('skills',)

    inlines = [SkillLevelInline]

    # class Meta:
    #     model = Employee
    #     fields = '__all__'

__staffmanager\workplaces\models.py__

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

__staffmanager\workplaces\admin.py__

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