from django.contrib import admin
from . import models
from . import forms


@admin.register(models.Professor)
class ProfessorAdmin(admin.ModelAdmin):
    form = forms.ProfessorCreationForm
    list_display = ["user", "first_name", "last_name", "department"]
    list_filter = ["department"]
    search_fields = ["user", "first_name", "last_name", "department"]
    ordering = ["department"]

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    form = forms.StudentCreationForm
    list_display = ["user", "first_name", "last_name", "department"]
    list_filter = ["department"]
    search_fields = ["user", "first_name", "last_name", "department"]
    filter_horizontal = ('courses_class',)
    ordering = ["department"]

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    form = forms.CourseCreationForm
    list_display = ["name", "department"]
    list_filter = ["department"]
    search_fields = ["name"]
    ordering = ["department"]


@admin.register(models.Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ["name", "number"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ["building", "capacity", "number"]
    search_fields = ["building", "number"]
    ordering = ["building"]


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["classroom", "start_class", "finish_class"]
    search_fields = [
        "classroom",
    ]
    ordering = ["classroom"]


@admin.register(models.CourseClass)
class CourseClassAdmin(admin.ModelAdmin):
    list_display = ["course", "schedule"]
    search_fields = [
        "course",
    ]
    ordering = ["course"]


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "building", "coordinator"]
    search_fields = ["name", "coordinator"]
    ordering = ["name"]

@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ["name", "course_class", "professor", "type_evaluation"]
    search_fields = ["name", "professor", "course_class"]
    ordering = ["name"]
    list_filter = ['type_evaluation']

admin.site.register(models.GradeEvaluation)
admin.site.register(models.TypeEvaluation)
