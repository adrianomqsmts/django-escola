from django import forms
from users.models import CustomUser
from . import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ProfessorCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_professor=True).all()
    )

    class Meta:
        model = models.Professor
        fields = "__all__"


class AlunoCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_professor=False).all()
    )

    class Meta:
        model = models.Aluno
        fields = "__all__"


class CursoCreationForm(forms.ModelForm):
    prerequisitos = forms.ModelMultipleChoiceField(
        queryset=models.Curso.objects.order_by("nome").all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = models.Curso
        fields = "__all__"


class AvaliacaoCreationForm(forms.ModelForm):

    valor = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        model = models.Avaliacao
        fields = ("nome", "tipo_avaliacao", "descricao", "valor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# class DisciplinaForm(forms.ModelForm):
    
#     class Meta:
#         model = models.Disciplina
#         fields = ("eh_finalizada",)

