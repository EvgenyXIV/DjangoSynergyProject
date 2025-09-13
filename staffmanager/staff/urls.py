from django.urls import path
from .views import (
    StaffListView,
    EmployeeDetailView,
    UserDetailView,
    UserListView,
    index,
)

app_name = "staff"  # имя приложения, которое будет использоваться в шаблонах

urlpatterns = [
    # для FBV представления
    # path('', index),                  # для FBV представления ссылка на функцю-обработчик staff/views/index.py
    # path('employee/<int:pk>/', detail),   # для FBV представления ссылка на функцю-обработчик staff/views/detail.py,
    # /<int:pk>/ - параметр пути в url для передачи в функцию-обработчик staff/views/detail.py
    # int - это конвертер типа пути, который преобразует строку в неотрицательное целое число
    # для CBV представления
    # используются классы EmployeeListView EmployeeDetailView в staff/views.py,
    # а в name= указывается 'user-list' 'user-detail' 'staff-list' 'employee-detail'- имена url-паттернов (в шаблонах),
    # /<int:pk>/ - параметр пути в url для встроенной функции-обработчик в классе DetailView
    # с конвертером int (строку в неотрицательное целое).
    # При необходимости изменения адреса страницы достаточно изменить адрес только в   path(''...   - имена url не меняются.
    path(
        "",
        UserListView.as_view(),
        name="user-list",
    ),  # URL страницы со списком пользователей
    path(
        "staff/",
        StaffListView.as_view(),
        name="staff-list",
    ),  # URL страницы со списком сотрудников
    path(
        "employee/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail",
    ),  # URL страницы с карточкой сотрудника
    path(
        "user/<int:pk>/",
        UserDetailView.as_view(),
        name="user-detail",
    ),  # URL страницы с карточкой пользователя
]
