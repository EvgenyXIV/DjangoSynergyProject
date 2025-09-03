# Создано виртуальное окружение python 3.12 в папке DjangoSynergyProject.venv 

python3.12 -m venv .venv
.venv/Scripts/activate

Установка Джанго версии 5.2.1.
py -m pip install Django==5.2.1

Установка автоформаттера black и сортировщика импортов isort
pip install black
python -m pip install isort

Создание Джанго-проекта staffmanager
django-admin startproject staffmanager

Создание Джанго-приложений staff (хранение инф. о персонале) и workplaces (хранение инф. о рабочих сестах)
cd  staffmanager
py manage.py startapp staff
py manage.py startapp workplaces

Регистрация приложений в settings.py
Application definition
INSTALLED_APPS = [
    # Регистрируем приложения учёта персонала и рабочих мест в наcтройках
    'staff',
    'workplaces',
.............
