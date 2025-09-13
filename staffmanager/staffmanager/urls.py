"""
URL configuration for staffmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

# импортируем модуль views из папки staff, содержащую функции-обработчики запросов
from staff import views

# импорт модуля debug_toolbar
import debug_toolbar

# Импорт редактора django-ckeditor-5
import django_ckeditor_5

# импорт модуля settings и функции static
# для настройки обработки медиа-файлов проекта в режиме debug
# Кроме этого, в шаблонах следует загружать тег {% load static %}
from django.conf import settings
from django.conf.urls.static import static


# Список всех адресов обработчиков запросов
urlpatterns = [
    # URL для обработчика staffmanager\staff\views.py\index()
    # path("", views.index),
    # Путь поиска ссылок в приложении staff для главной страницы
    path("", include("staff.urls")),
    # URL для обработчика из модуля admin.py
    path("admin/", admin.site.urls, name="admin"),
    # URL для обработчика из проекта DjDt
    path("__debug__/", include(debug_toolbar.urls)),
    # URL для редактора django-ckeditor-5
    path("admin/", include("django_ckeditor_5.urls")),
]

"""
Эта настройка для работы с медиа файлами только в режиме разработки проекта: если DEBUG = True.
Если DEBUG = False, то функция static() не будет работать.
static() - возвращает путь к медиа файлу, если он существует.
"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
