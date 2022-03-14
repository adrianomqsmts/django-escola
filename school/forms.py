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


class StudentCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_professor=False).all()
    )
    courses = forms.ModelMultipleChoiceField(
        queryset=models.Course.objects.order_by('department').all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = models.Student
        fields = "__all__"


class CourseCreationForm(forms.ModelForm):
    prerequisites = forms.ModelMultipleChoiceField(
        queryset=models.Course.objects.order_by('department').all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = models.Course
        fields = "__all__"
        
        

class EvaluationCreationForm(forms.ModelForm):
    
    value = forms.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])
    
    class Meta:
        model = models.Evaluation
        fields = ('name','type_evaluation',  'description', 'value')