from django.contrib import admin
from .models import Employee, EmployeeImage, Skill, SkillLevel

# Для добавления полей модели сотрудника-пользователя на страницу  пользователя
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

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


# Регистрируем модель EmployeeImage в админке
@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    class Meta:
        model = EmployeeImage
        fields = "__all__"
        extra = 3


# Регистриуем инлайн для изображений сотрудника в админке в табличном виде
class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage


@admin.register(
    Employee
)  # Регистрируем модель Employee  c инлайном навык(уровень) админке
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
        "role",
        "employment_date",
        "employment_days",
        "employee_skills",
        "workplace",
        "description",
    )
    list_editable = (
        "first_name",
        "middle_name",
        "last_name",
        "role",
        "employment_date",
        "workplace",
        "description",
    )
    search_fields = ("last_name",)
    list_filter = ("skills",)
    list_display_links = ("id",)
    # filter_horizontal = ('skills',)

    inlines = [SkillLevelInline, EmployeeImageInline]

    # class Meta:
    #     model = Employee
    #     fields = '__all__'



