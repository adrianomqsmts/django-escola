from django.contrib import admin
from . import models
from . import forms


@admin.register(models.Professor)
class ProfessorAdmin(admin.ModelAdmin):
    form = forms.ProfessorCreationForm
    list_display = ["user", "first_name", "last_name", "departamento"]
    list_filter = ["departamento"]
    search_fields = ["user", "first_name", "last_name", "departamento"]
    ordering = ["departamento"]

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


@admin.register(models.Aluno)
class AlunoAdmin(admin.ModelAdmin):
    form = forms.AlunoCreationForm
    list_display = ["matricula","user", "first_name", "last_name"]
    search_fields = ["matricula", "user", "first_name", "last_name"]
    filter_horizontal = ['disciplinas']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


@admin.register(models.Curso)
class CursoAdmin(admin.ModelAdmin):
    form = forms.CursoCreationForm
    list_display = ["codigo", "nome", "departamento"]
    list_filter = ["departamento"]
    search_fields = ["codigo", "nome"]
    ordering = ["codigo", "nome", "departamento"]
    list_display_links = ["codigo", "nome"]


@admin.register(models.Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    autocomplete_fields  = ("curso", "professor", "horario")
    list_display = ["curso","horario", "ano", "semestre", "professor", "eh_finalizada"]
    search_fields = ["professor", "semestre", "curso__nome", "horario__predio", "ano"]
    list_filter = ["eh_finalizada"]
    ordering = ["ano"]


@admin.register(models.Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ["nome", "disciplina", "tipo_avaliacao"]
    search_fields = ["nome", "disciplina"]
    ordering = ["nome"]
    list_filter = ['tipo_avaliacao']


@admin.register(models.Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ["predio", "porta", "capacidade", "tem_projetor"]
    list_filter = ["tem_projetor"]


@admin.register(models.Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ["sala", "inicio", "termino"]
    search_fields = ["sala__predio", "sala__porta"]
    

@admin.register(models.TipoAvaliacao)
class TipoAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ["nome", "descricao"]
    ordering = ["nome"]
    
    



@admin.register(models.Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ["nome", "coordenador"]
    ordering = ["nome"]
    
    
admin.site.register(models.Nota)
admin.site.register(models.Semestre)