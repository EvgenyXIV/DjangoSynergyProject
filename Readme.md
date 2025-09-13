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

#Create your models here.


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

*******************ДЗ 3   Представления (views) и шаблоны (templates)***********************************


Настройки шаблонов
__Подключить статические и медиа файлы Подключить шаблоны на уровне проекта__

В этом проекте для пользовательского интерфейса были выбраны представления
на основе классов Class-Based Views (CBV).
Использовались два класса представлений, встроенных в Django:
DetailView  - страница подробных сведений об объекте в модели базе данных;
ListView    - страница списка объектов модели базы данных.

На уровне проекта staffmanager были созданы ллокальные папки:
staffmanager\media      - локальная папка для хранения файлов пользователей;

staffmanager\static_dev - локальная папка для хранения статических файлов (подапки css, js, img, files);

staffmanager\templates  - для хранения шаблонов приложений, базовый шаблон base.html в корне папки,
                          подппапка staff с наследниками базового шаблона employee_detail.html и employee_list.html,
                          подпапка includes для шаблонов сторонних приложений;

__ФАЙЛ staffmanager\staffmanager\settings.py:__
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",   # Подключен Джанго-шаблонизатор (DjangoTemplates). 
                                                                        # Но можно использовать и Jinja2
        "DIRS": [BASE_DIR / 'templates'], # 'DIRS': [] поиск шаблонов по умолчанию будет в подпапке templates/app_name в папке приложения
                                          # или 'DIRS': [BASE_DIR / 'templates'] в указанной папке для хранения шаблонов в папке проекта BASE_DIR/,
        "APP_DIRS": True,                 # True - поиск шаблонов в папке приложения после поиска в папке проекта
    .................
    }
........................
]
STATIC_URL = "static/"        # Задано имя URL для статических файлов, которые будут доступны по адресу BASE_DIR / 'static_dev'
STATICFILES_DIRS = [
    BASE_DIR / "static_DEV",  # Локальная папка на уровне проекта static_dev для хранения статических файлов (подапки css, js, img, files..)
                              # Перед использованием в шаблонах надо загрузить тег {% load static %} в шаблонах
]

MEDIA_URL = 'media/'             # # Задано имя URL для загрузки файлов пользователями
MEDIA_ROOT = BASE_DIR / 'media'  # адрес локальной папки для хранения файлов пользователей

__ФАЙЛ staffmanager\staff\views.py:__

from .models import Employee
from django.contrib.auth.mixins import LoginRequiredMixin # для защиты доступа к страницам (для авторизованного пользователя,  
                                                          # например, для личного кабинета или для дилеров, или ...). 
                                                          # Указывается на первом месте в атрибутах класса
from django.views.generic import DetailView, ListView

"""
ПРЕДСТАВЛЕНИЕ CBV:
Для веб-интерфейса модели Employee используем встроенные классы ListView и DetailView
импортируем классы ListView и DetailView, модель Employee.
Имена шаблонов будут по умолчанию:
"""

class BookListView(LoginRequiredMixin, ListView):
    model = Employee

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Employee

__ФАЙЛ staffmanager\staffmanager\urls.py__

from django.contrib import admin
from django.urls import include, path

#импорт модуля debug_toolbar
import debug_toolbar

#Импорт редактора django-ckeditor-5
import django_ckeditor_5

#импорт модуля settings и функции static
#для настройки обработки медиа-файлов проекта в режиме debug
from django.conf import settings
from django.conf.urls.static import static  

#Список всех адресов обработчиков запросов
urlpatterns = [

    # Путь поиска ссылок в приложении staff для главной страницы
    path("", include("staff.urls")),
    # URL для обработчика из модуля admin.py
    path("admin/", admin.site.urls),
    # URL для обработчика из проекта DjDt
    path(
        "__debug__/", include(debug_toolbar.urls)
    ),
  
    # URL для редактора django-ckeditor-5    
    path(
        "admin/", include("django_ckeditor_5.urls")
    ),
    
]

"""
Эта настройка для работы с медиа файлами только в режиме разработки проекта: если DEBUG = True.
Если DEBUG = False, то функция static() не будет работать.
static() - возвращает путь к медиа файлу, если он существует.
"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

__ФАЙЛ staffmanager\staff\urls.py__

from django.urls import path
from .views import EmployeeListView, EmployeeDetailView

app_name = 'staff'  # имя приложения, которое будет использоваться в шаблонах

urlpatterns = [
    # для CBV представления
    # используются классы EmployeeListView EmployeeDetailView в staff/views.py,
    # а в name= указывается 'employee_list' 'employee_detail'- имена url (в шаблонах),
    # /<int:pk>/ - параметр пути в url для встроенной функции-обработчик в классе DetailView 
    # с конвертером int (строку в неотрицательное целое).
    # При необходимости изменения адреса страницы достаточно изменить адрес только в   path(''...  ) - имена url не меняются.
    path('', EmployeeListView.as_view(), name='employee_list',),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail',), 
]

__Модели__

Установка стороннего приложения django-cleanup
для физического удаления файлов (например - фотографий из галерей сотрудников)
после удаления ссылок на них в админке или удаления моделей.
ВАЖНО! Приложение django_cleanup должно быть последним в списке установленных приложений

>>> pip install django-cleanup
INSTALLED_APPS = (
    ...,
    'django_cleanup.apps.CleanupConfig',
)

Установка библиотеки Pillow для обработки изображений.
>>>python -m pip install Pillow

staffmanager\staff\models.py:
-Добавляем модель EmployeeImage с отношением многие к одному с моделью Employee.
-Добавляем поля "is_main" - главное изображение (True, False) 
 и "order" - порядковый номер (неотрицательное) для ранжирования и сортировки

-Определяем в модели EmployeeImage функцию save(self, *args, **kwargs) сохранения изображений
 с установкой единого размера изображений 300х300 пикселей - используется библиотека Pillow
-При назначении нового или уже существующего изображения главным  
 прежнее главное изображение меняет этот признак на False.

 #Переопределяем метод сохранения изображения (Pillow)
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        if self.is_main: #Если новый признак фото "главное", то всем остальным главным меняем атрибут is_main=False
            EmployeeImage.objects.filter(employee=self.employee, is_main=True).exclude(pk=self.pk).update(is_main=False)
        if self.image:
            img = PILImage.open(self.image.path)
            img = img.resize([300, 300]) # Устанавливаем размер изображения
            img.save(self.image.path) # Сохраняем изменённое изображение
            return self.image

staffmanager\staff\admin.py:
 #Регистрируем модель EmployeeImage в админке с выводом всех полей
@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    class Meta:
        model = EmployeeImage
        fields = '__all__'

 #Регистриуем инлайн для изображений сотрудника в админке в табличном виде
class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage

staffmanager\templates\includes\employee_header.html

В шаблоне вывода карточки сотрудника первым выводим главное изоражение и
добавляем вывод всех остальных изображений в порядке order

 Изображения:
<ul>
    {% for image in employee.employee_gallery.all %}
        {% if image.is_main %}
            <img src="{{ image.image.url }}" alt="PHOTO" style="border: 8px solid red;">
         {% endif %}
            {% endfor %}
</ul>
<ul>
    {% for image in employee.employee_gallery.all %}
        {% if image.image %}
            {% if not image.is_main %}
                <img src="{{ image.image.url }}" alt="PHOTO">
            {% endif %}
        {% else %}
            <p> "нет изображения, добавьте изображение или удалите объект" </p>
            {% endif %}
    {% endfor %}

__Шаблоны, представления и адреса:__

Все представления выполнены по подходу CBV. 
Рабочие файлы представлений были описаны выше.

В проекте Django кроме страниц админки организованы страницы:
-главная страница со списков всех пользователей  http://127.0.0.1:8000/
-страница со списком всех сотрудников   http://127.0.0.1:8000/staff/
-страница подробных сведений о пользователе http://127.0.0.1:8000/user/pk=user_id/
-страница подробных сведений о сотруднике    http://127.0.0.1:8000/employee/pk=employee_id/

Все шаблоны и статические файлы расположены на уровне проекта staffmanager/
и имеют стандартную архитектуру.

Папка staffmanager\static_dev содержит статические файлы. Подпапки css files img js.
Папка staffmanager содержит базовый шаблон base.html
Папка staffmanager\templates\staff содержит шаблоны-наследники для приложения staff.
Папка staffmanager\templates\includes содержит шаблоны для вставки в базовом шаблоне или в его наследниках

Для всех страниц проекта шаблоны наследуются от базового шаблона base.html, который:
-определяет одинаковый титул для всех страниц,
-выводит логотип Синергии,
-определяет поле блок-контента для наследников и
-создаёт две ссылки для перехода на главную страницу и на страницу списка сотрудников.

Для читабельности основных шаблонов громоздкие блоки были выведены в папку includes в виде отдельных шаблонов.
а в основных шаблонах вставлены ссылки на них. Пример:
В employee_detail.html:
{% include 'includes/employee_header.html' %}


На главной странице http://127.0.0.1:8000/ (шаблон )
-выводится список всех пользователей с использованием данных из встроенной модели пользователя User
-в списке пользователей созданы кнопки для перехода на страницу карточки подробных сведений о пользователе
Пример:
ПОДРОБНОСТИ О ПОЛЬЗОВАТЕЛЕ
/static/css/index.css
ПОЛЬЗОВАТЕЛЬ: user1
user.username - user1
user.password - pbkdf2_sha256$1000000$8VyAT9hx5zntiE2gBC2APc$WPl12Lhh7XkSyuucJuF/2HOuIbu5m+f1jIciGVt/r8Q=
user.email -
user.first_name -
user.last_name -
user.groups - auth.Group.None
user.user_permissions - auth.Permission.None
user.is_staff - True
user.is_superuser - True
user.is_active - True
user.date_joined - 5 сентября 2025 г. 6:24
user.last_login - 12 сентября 2025 г. 9:38

На странице сотрудников http://127.0.0.1:8000/staff/
-выводится список всех сотрудников с использованием данных из модели сотрудника Employee
-в списке сотрудников созданы кнопки для перехода на страницу карточки подробных сведений о сотруднике

Для оптимизации запросов к базе при выводе списка связанных объектов
(навык, уровень) из модели сотрудников Employee
в классе EmployeeDetailView (модуль staff/views.py)
была написана специальная функция get_queryset(self) :

    def get_queryset(self):
        return Employee.objects.prefetch_related('skilllevel_set').all()

Менеджер запроса к базе Employee.objects использует метод .prefetch_related,
выполняющий предварительную загрузку всех связанных отношением many-to many объектов,
а метод .all() возвращает список skilllevel_set из всех связанных объектов запроса.
Таким образом, имеем один запрос к базе вместо нескольких запросов.

Вывод навыков в шаблоне staffmanager\templates\includes\employee_header.html в цикле for:
<ul>
    {% for skill_ in employee.skilllevel_set.all %}
        <li>
            {{ skill_.skill.name }} ({{ skill_.level }})
        </li>
        {% empty %}
            <li>Нет навыков</li>
    {% endfor %}
</ul>

Пример:
ПОДРОБНОСТИ О СОТРУДНИКЕ
/static/css/index.css
СОТРУДНИК: user2 user2
user.username - user1
employee.user_id - 2
employee.email -
employee.first_name - user2
employee.last_name - user2
employee.gender - female
employee.workplace - Рабочее место №7
employee.description - <p>Сотрудница успешно прошла стажировку и работает в команде с 2021 года.&nbsp;</p>

Навыки(уровень):

фронтенд (1)
тестирование (2)
управление проектами (5)

Страницы подробных сведений о сотрудниках и пользователях доступны только авторизованным пользователям. 
Для контроля доступа к страницам использовался встроенный в Django класс LoginRequiredMixin
при создании классов path-паттернов в модуле staff/view.py:
class UserDetailView(LoginRequiredMixin, DetailView):
...........

class EmployeeDetailView(LoginRequiredMixin, DetailView):
...........

Обновлены зависимости в файле requirements.txt:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject> pip freeze > requirements.txt

Рабочие файлы были отформатированы форматтером black:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject> black staffmanager\
