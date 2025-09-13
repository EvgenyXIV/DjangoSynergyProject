from django.shortcuts import render
from django.http import HttpResponse
from .models import (
    Employee,
)  # Импортируем модели Employee, SkillLevel, Skill

from django.contrib.auth.models import User  # Импортируем модель User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)  # для защиты доступа к страницам (для авторизованного пользователя,

# например, для личного кабинета или для дилеров, или ...).
# Указывается на первом месте
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

'''
"""Для простоты вместо html шаблона используем класс HttpResponse - из пакета позволяет отправить текстовое содержимое.
Функция-обработчик index() принимает запрос request и возвращает ответ 'Здесь будет главная страница'  в теге h1 - заголовок первого уровня.
Для вызова этой функции-обработчика надо в Джанго-проекте staffmanager в urls.py внести в список адресов urlpatterns
адрес path('',views.index), по которому она находится. 
Путь 'staffmanager.urls' к файлу с адресами urls.py содержится в переменной ROOT_URLCONF в настройках проекта staffmanager в файле settings.py """
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("<h1>Здесь будет главная страница<h1>")
'''

"""
ЭТИ ФУНКЦИИ index(request):  detail(request, pk): ДЛЯ WEB-интерфейса модели Book ПРИ ПРЕДСТАВЛЕНИИ FBV
"""


def index(request):
    template_name = "staff/index.html"
    try:
        context = {"staff": Employee.objects.all}
    except:
        context = {"staff": "список сотрудников пустой"}
    return render(request, template_name, context)


def detail(request, pk):
    template_name = "staff/detail.html"
    try:
        context = {"book": Employee.objects.get(pk=pk)}
    except:
        context = {"employee": "такого сотрудника нет в списке"}
    return render(request, template_name, context)


"""
ПРЕДСТАВЛЕНИЕ CBV:
Для веб-интерфейса модели Employee используем встроенные классы ListView и DetailView
импортируем классы ListView и DetailView, модель Employee.
Имена шаблонов будут по умолчанию employee_detail.html и employee_list.html:
"""


# Класс ListView для отображения списка пользователей
class UserListView(ListView):
    template_name = "staff/user_list.html"
    model = User


# Класс ListView для отображения списка сотрудников
class StaffListView(ListView):
    # template_name = 'staff/index.html' # для шаблонов на уровне приложения staffmanager\staff\templates\staff\index.html
    # в приложении (model_name_list.html = employee_list.html)
    # context_object_name = 'staff'      # для шаблонов на уровне приложения имя переменной в шаблоне \staff\templates\staff\index.html,
    # в которой будут передаваться объекты (по умолчанию 'object_list')
    model = Employee


# Класс DetailView для отображения информации о пользователе
class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "staff/user_detail.html"  #  для шаблонов на уровне приложения (staff/templates/staff/user_detail.html)
    model = User


# Класс DetailView для отображения информации о сотруднике
class EmployeeDetailView(LoginRequiredMixin, DetailView):
    # template_name = 'staff/employee_detail.html' #  для шаблонов на уровне приложения (staff/templates/staff/employee_detail.html)
    model = Employee

    # Функция для получения списка scillevel_set всех свойств сотрудника, связанных с другими таблицами проекта
    # (это навыки, их описания и уровени навыков)  для отображения через шаблон страницы подробных сведений о сотруднике
    def get_queryset(self):
        return Employee.objects.prefetch_related("skilllevel_set").all()
