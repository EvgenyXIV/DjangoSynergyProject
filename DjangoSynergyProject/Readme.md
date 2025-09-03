# Создано виртуальное окружение python 3.12 в папке DjangoSynergyProject.venv 

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