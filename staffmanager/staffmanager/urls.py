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

# Список всех адресов обработчиков запросов
urlpatterns = [
    path("admin/", admin.site.urls),  # URL для обработчика из модуля admin.py
    path(
        "__debug__/", include(debug_toolbar.urls)
    ),  # URL для обработчика из проекта DjDt
    path("", views.index),  # URL для обработчика index()
    path(
        "admin/", include("django_ckeditor_5.urls")
    ),  # URL для редактора django-ckeditor-5
    # path('admin/image_upload', include('django_ckeditor_5.urls')), # URL для редактора django-ckeditor-5
]
