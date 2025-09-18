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
]
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

 #Регистрируем инлайн для изображений сотрудника в админке в табличном виде
class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage

staffmanager\templates\includes\employee_header.html

В шаблоне вывода карточки сотрудника первым выводим главное изоражение в красной рамке и
добавляем вывод всех остальных изображений в порядке order

 Изображения:
<ul>
    {% for image in employee.employee_gallery.all %} # Перебираем все изображения
        {% if image.is_main %}                       # Если это главное изображение
            <img src="{{ image.image.url }}" alt="PHOTO" style="border: 8px solid red;">    # выводим главное изображение в красной рамке
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


*******************ДЗ 4   Запросы в БД****************************

1. Добавить к модели сотрудника поля с датой приёма на работу и стаж в днях.

Для расчёта стажа переопределим метод модели save(). 
Стаж будет перерассчитываться при сохранении сотрудника, это поле будет не редактируемо.
Дата приёма на работу косвенно валидируется стажем.
Стаж неотрицателен - поэтому дата приёма на работу !!не может!! превышать текущую дату - возникнет !!!ошибка по стажу!!

***staffmanager\staff\models.py:***

class Employee(models.Model):  # Класс Сотрудник наследник базовой модели Model
............
    # Дата приёма на работу
    employment_date = models.DateField(verbose_name="Дата приёма на работу", blank=True, null=True)
    # Стаж в днях
    employment_days = models.PositiveIntegerField(verbose_name="Стаж в днях", blank=True, null=True, default=0, editable=False)
..............
    Выполним миграцию БД

    Изменим админку - добавим в отображение столбцы приёма на работу и стажа

***staffmanager\staff\admin.py***

    list_display = (
..................
        "employment_date",
        "employment_days",
....................
    )
    list_editable = (
........................
        "employment_date",
..........................
    )

    Изменим шаблон карточки сотрудника - добавим вывод приёма и стажа

***staffmanager\templates\includes\employee_header.html***

            СОТРУДНИК: {{ employee.first_name }} {{ employee.last_name }}
            <ul>
...............................................................................
                <li>Дата приёма на работу - {{ employee.employment_date }}</li>
                <li>Стаж в днях - {{ employee.employment_days }}</li>
.................................................................................
            </ul>

2. Создать  валидатор, который не допускает нахождение тестировщиков и разработчиков за соседними столами.
    Для этого  в модели Employee:
    ***staffmanager\staff\models.py***
    - импортируем встроенный в Django класс ValidationError
        from django.core.exceptions import ValidationError
    
    - создадим поле role с выбором ролей(должностей) у сотрудников из списка ROLES.
        class Employee(models.Model):
            ROLES = (
        ('frontend-developer','фронтенд разработчик'),
        ('backend-developer','бэкенд разработчик'), 
        ('qa-engineer', 'тестировщик'), 
        ('project-manager','руководитель проекта'), 
        ('prompt engineer', 'промпт-инженер'),
        ('other', 'другое'),
    )
        role = models.CharField(choices=ROLES, verbose_name="Роль", default='other', blank=True, null=True)

    - Напишем метод-валидатор def validate_workplace(self):, в котором получаем текущий номер рабочего места через запрос по связанному
        ОДИН К ОДНОМУ полю workplace,
        по списку из двух номеров соседних мест получаем сотрудников для этих мест через запрос к модели сотрудника Employee 
        с пробросом  к данным из связанной ОДИН К ОДНОМУ модели рабочего места Workplace. Формат проброса двойное нижнее подчеркивание:
        Employee.objects.filter(workplace__table__in=neighbour_workplaces). 
        
        Затем по ролям текущего сотрудника и его соседей работает логика валидации из нескольких логических конструкций,
        в результате которой возникают сообщения о недопустимом соседстве 
        с указанием соседа, его роли и номера его места и сохранение модели сотрудников не происходит.
        
        Для запуска пользовательского метода-валидатора служит встроенный метод  валидации clean(). 
        Дополнительно, при окончании пользовательской валидации рабочих мест  в методе save() вызывается 
        встроенный метод полной валидации модели full_clean() перед продолжением сохранения модели

         #Переопределяем метод сохранения
        def save(self, *args, **qkwargs):   
        .....................................
        self.full_clean()  # Проверяем валидность модели перед сохранением
        super().save(*args, **qkwargs)  # Продолжаем сохранять базовым методом модели

        #Переопределяем метод валидации
        def clean(self):
        self.validate_workplace()

            # Метод для валидации рабочего места
    def validate_workplace(self):
        place = self.workplace.table # Получаем номер рабочего места
        neighbour_workplaces = [place - 1, place + 1] # Соседние рабочие места
        neighbours = Employee.objects.filter(workplace__table__in=neighbour_workplaces)    # Сотрудники на соседних рабочих местах
        if self.role == "qa-engineer":  # Если сотрудник тестировщик
            for neighbour in neighbours:
                if neighbour.role == "frontend-developer":    # Если соседний сотрудник фронтенд разработчик
                    raise ValidationError(f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом")
                elif neighbour.role == "backend-developer":  # Если соседний сотрудник бэкенд разработчик
                    raise ValidationError(f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом")
        if self.role == "frontend-developer" or self.role == "backend-developer":  # Если сотрудник разработчик
            for neighbour in neighbours:
                if neighbour.role == "qa-engineer":    # Если соседний сотрудник тестировщик
                    raise ValidationError(f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом")
                
    - необходимо сделать миграцию базы данных.

    В админке сотрудника  прописываем в списках выводимых и редактируемых атрибутов роль сотрудника для вывода на общий экран
    ***staffmanager\staff\admin.py***
        list_display = (
.................
        "role",
 ................
    )
    list_editable = (
....................
        "role",
..................
    )

3. На главной странице добавить и вывести в произвольном месте шаблона страницы сотрудников общее
количество сотрудников в базе данных.
4. На главной странице вывести карточки только 4-х последних по дате приёма работы
сотрудников. 
На главной странице и в Списке всех сотрудниковВ карточку сотрудника добавить стаж работы в компании в днях
5. В Списке всех сотрудников вывести карточки сотрудников с пажинацией по 2 на странице.

В базовом шаблоне добавляем ссылки 
"На главную" на страницу http://127.0.0.1:8000/ со списком 4х последних нанятых сотрудников 
"На список сотрудников" на страницу staff/ всех сотрудников

***staffmanager\templates\base.html***
<a href="{% url 'staff:staff-last4' %}">На главную</a>
<a href="{% url 'staff:staff-list-all' %}">На список сотрудников</a></br>

В паттернах path в urls.py в приложении staff
задаём шаблон главной страницы http://127.0.0.1:8000/  
и страницы /staff списка всех сотрудников  

***staffmanager\staff\urls.py***
path("staff/", StaffListView.as_view(), name="staff-list-all",),    # URL страницы со списком всех сотрудников
path("", StaffListView.as_view(), name="staff-last4", ),            # URL главной страницы со списком 4х недавно принятых сотрудников

В представлениях приложения staff переопределяем метод get_context_data для модели StaffListView

***staffmanager\staff\views.py***
в модели StaffListView
class StaffListView(ListView):
-добавляем пагинацию по 2 записи на странице всех сотрудников:
-----------------------------------
     paginate_by = 2 # Число записей на странице
-----------------------------------     

 Переопределяем метод get_context_data и пишем код для выбора типа списка сотрудников при клике на ссылки на страницы.
При клике на ссылку "На главную" откроется страница http://127.0.0.1:8000/ со списком 4х последних нанятых сотрудников
При клике на ссылку "На список сотрудников" окроется страница staff/ всех сотрудников
В шаблоне staffmanager\templates\staff\employee_list.html в цикле for надо использовать список сотрудников с именем staff

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) # Получаем базовый контекст запроса в виде словаря из класса ListView
    context['staff_list_length'] = self.model.objects.count() - агрегацию общего числа сотрудников count()
    context['staff_last4'] = self.model.objects.order_by('-employment_date')[:4] -  список последних 4х сотрудников,
                                                                                    отсортированных по дате приёма DSC 
                                                                                    (знак "-" перед именем поля сортировки)
    pattern_name = self.request.resolver_match.url_name # Получаем имя url-паттерна при клике на ссылку в базовом шаблоне base.html
    if pattern_name == 'staff-last4': 
        context['staff'] =  context['staff_last4']
    elif pattern_name == 'staff-list-all':
        context['staff'] =  context['object_list']

В шаблоне главной страницы employee_list.html размещаем обработку этих  контекст-данных {{ staff_list_length }} и {{ staff_last4 }} 
и, используя имя контекстного списка context['staff'], выводим в цикле for требуемые данные сотрудника employee
***staffmanager\templates\staff\employee_list.html***
    <h1>СПИСОК СОТРУДНИКОВ.</h1>
    <h1>Всего сотрудников: {{ staff_list_length }}</h1>
    <h2>{{ staff_last4 }}</h2></br></br>
    ----------------------------------------------
     {% for employee in staff %}
    <li>
        {% include 'includes/employee_card.html' %} 
    -----------------------------------------------

Добавляем код для перехода по страницам при пагинации
***staffmanager\templates\staff\employee_list.html***
        <!-- Пагинация -->
    <div class="pagination">
        {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}">Предыдущая</a>
        {% endif %}
        
        Страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}
        
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Следующая</a>
        {% endif %}
    </div>

В инклюде в шаблон главной страницы выводим имя фамилию и стаж в днях сотрудника и ссылку "подробнее" на подробную карточку сотрудника 

***staffmanager\templates\includes\employee_card.html***
    <b>{{ forloop.counter1 }}.</b> Сотрудник: {{ employee.first_name }} {{ employee.last_name }}
            Стаж в Компании, дней ={{ employee.employment_days }}
    <a href="{% url 'staff:employee-detail' employee.id %}">Подробнее</a><br>

6. На Главной странице и в Списке всех сотрудников в карточку сотрудника добавить имя, фамилию, стаж в днях и главное изображение галереи
сотрудника.

Для вывода главного изображения сотрудника 
- методом .get(is_main=True)  получаем главное изображение для каждого сотрудника из списка context['staff']
- сохраняем его в объекте main_image. Оно у сотрудника единственное (если есть)
- передаём объект main_image в карточку сотрудника employee

class StaffListView(ListView):
--------------------------------------------
def get_context_data(self, **kwargs):
-----------------------------------------------
    for employee in context['staff']: 
        try:
            main_image = employee.employee_gallery.get(is_main=True)        # Получаем главное изображение сотрудника
            employee.main_image = main_image                                # передаём в карточку  сотрудника его главное изображение 
        except Exception: print(f"employee.id {employee.id} None image")    # Вывод в терминал "None image", если нет главного изображения
    return context                                                          # Возвращаем полученный контекст в шаблон
---------------------------------------------------

В инклюд-шаблоне  staffmanager\templates\includes\employee_card.html для шаблона staffmanager\templates\staff\employee_list.html
***staffmanager\templates\includes\employee_card.html***
<b>{{ forloop.counter }}.</b>  Сотрудник: {{ employee.first_name }} {{ employee.last_name }} Стаж в Компании, дней ={{ employee.employment_days }}
    <!--Путь к фото upload_to="employee_images/" указан в image - экземпляре класса ImageField() в модели EmployeeImage-->
    <!-- выводим главное изображение в красной рамке из контекстного объекта main_image -->
    <img src="{{ employee.main_image.image.url }}" alt="PHOTO" style="border: 8px solid red;"></br></br>  

7. Подробная карточка сотрудника
Добавьте в контекст и разместите в шаблоне главное изображение сотрудника. 


Для вывода главного изображения сотрудника (CBV класс ass EmployeeDetailView(LoginRequiredMixin, DetailView)):
- методом .get(is_main=True)  получаем главное изображение сотрудника
- сохраняем его в контекст-объекте context['main_image']. Оно у сотрудника единственное (если есть)

EmployeeDetailView(LoginRequiredMixin, DetailView):
--------------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.employee_gallery.get(is_main=True)   # Получаем в карточку сотрудника главное изображение
        return(context)                                                          # Возвращаем полученный контекст в шаблон
-----------------------------------------------

В инклюд-шаблоне  staffmanager\templates\includes\employee_header.html для шаблона staffmanager\templates\staff\employee_detail.html
***staffmanager\templates\includes\employee_header.html***
            <!--Путь к фото upload_to="employee_images/" указан в image - экземпляре класса ImageField() в модели EmployeeImage-->
            <!-- выводим главное изображение в красной рамке из контекстного объекта main_image -->
            <img src="{{ main_image.image.url }}" alt="PHOTO" style="border: 8px solid red;">

Выводим имя, фамилия, пол, навыки с уровнями освоения, стаж в днях, номер стола,галерея изображений (без первого).

Это было сделано в ДЗ 3   Представления (views) и шаблоны (templates)
через перебор изображений в цикле for с исключением из вывода главного изображения
***staffmanager\templates\includes\employee_header.html***

        <!-- Получаем данные сотрудника из встроенной модели Employee и выводим их списком -->
        СОТРУДНИК: {{ employee.first_name }} {{ employee.last_name }}</br>
            <ul>
                <li>user.username - {{ user.username}}</li>
                <li>employee.user_id - {{ employee.user_id }}</li>
                <li>email - {{ employee.email }}</li>
                <li>Имя - {{ employee.first_name }}</li>
                <li>Фамилия - {{ employee.last_name }}</li>
                <li>Пол - {{ employee.gender }}</li>
                <li>Дата приёма на работу - {{ employee.employment_date }}</li>
                <li>Стаж в днях - {{ employee.employment_days }}</li>
                <li>Номер стола - {{ employee.workplace }}</li>
                <li>Описание - {{ employee.description }}</li>
            </ul>
            Навыки(уровень):
            <ul>
                {% for skill_ in employee.skilllevel_set.all %}
                    <li>
                        {{ skill_.skill.name }} ({{ skill_.level }})
                    </li>
                    {% empty %}
                        <li>Нет навыков</li>
                {% endfor %}
            </ul>
            Изображения:
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
            </ul>

