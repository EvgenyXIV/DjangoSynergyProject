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

# Список всех адресов обработчиков запросов
urlpatterns = [
    path('admin/', admin.site.urls),                  # URL для обработчика из модуля 
    path('__debug__/', include(debug_toolbar.urls) ), # URL для обработчика из другого джанго-проекта    
    path('',views.index)                              # URL для обработчика index() 
]
