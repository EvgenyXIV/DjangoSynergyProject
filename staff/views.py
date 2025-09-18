from django.shortcuts import render
from django.http import HttpResponse
from .models import (
    Employee,
     SkillLevel, 
     Skill,
     EmployeeImage,
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
    #template_name = "staff/user_list.html" # Задаем имя и адрес  шаблона user_list.html для вывода списка пользователей
    model = User # шаблон страницы по умолчанию: staffmanager\templates\staff\user_list.html


# Класс ListView для отображения списка сотрудников
class StaffListView(ListView):
    # template_name = 'staff/index.html' #  Задаем имя и адрес  шаблона index.html для вывода списка сотрудников
    # в приложении (model_name_list.html = employee_list.html)
    # context_object_name = 'staff'      # для шаблонов на уровне приложения имя переменной в шаблоне \staff\templates\staff\index.html,
    # в которой будут передаваться объекты (по умолчанию 'object_list')
    model = Employee # шаблон страницы по умолчанию: staffmanager\templates\staff\employee_list.html
    context_object_name = 'staff'
    paginate_by = 2 # Число записей на странице
    
    #class Meta:
    #    ordering = ('employment_date')  # Упорядочиваем вывод сотрудников по дате приёма на работу

    
    # Переопределяем метод get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Получаем базовый контекст запроса в виде словаря из класса ListView
        context['staff_last4'] = self.model.objects.order_by('-employment_date')[:4] # Добавляем в контекст список последних 4х сотрудников, принятых на работу
        context['staff_list_length'] = self.model.objects.count() # Добавляем в контекст количество сотрудников через агрегацию .count(). 
        
        # Выбор типа списка сотрудников на главной странице и на странице staff/.
        # В шаблоне staffmanager\templates\staff\employee_list.html в цикле for надо использовать список сотрудников с именем staff
        pattern_name = self.request.resolver_match.url_name # Получаем имя url-паттерна при клике на ссылку в базовом шаблоне base.html
        if pattern_name == 'staff-last4': 
            context['staff'] =  context['staff_last4']
        elif pattern_name == 'staff-list-all':
            context['staff'] =  context['object_list']

        # Для каждого сотрудника в списке получаем в карточку главное изображение. Оно у сотрудника единственное (если есть)
        for employee in context['staff']:  #
            try:
                main_image = employee.employee_gallery.get(is_main=True)   # Получаем в карточку сотрудника его главное изображение
                employee.main_image = main_image
            except Exception: print(f"employee.id {employee.id} None image") # Вывод в терминал, если нет главного изображения
        return context # Возвращаем полученный контекст в шаблон
    

# Класс UserDetailView для отображения информации о пользователе
class UserDetailView(LoginRequiredMixin, DetailView):
    # template_name = "staff/user_detail.html"  #  Задаем имя и адрес  шаблона user_detail.html для вывода информации о пользователе
    model = User    # шаблон страницы по умолчанию: staffmanager\templates\staff\user_detail.html


# Класс EmployeeDetailView для отображения информации о сотруднике
class EmployeeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'staff/employee_detail.html' #  Задаем имя и адрес шаблона employee_detail.html для вывода информации о сотруднике
    model = Employee    # шаблон страницы по умолчанию: staffmanager\templates\staff\employee_detail.html

    # Функция для получения списка scillevel_set всех свойств сотрудника, связанных с другими таблицами проекта
    # (это навыки, их описания и уровени навыков)  для отображения через шаблон страницы подробных сведений о сотруднике
    def get_queryset(self):
        return Employee.objects.prefetch_related("skilllevel_set").all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.employee_gallery.get(is_main=True)  # Получаем в карточку сотрудника главное изображение
        return(context)                                                         # Возвращаем полученный контекст в шаблон
        
    
