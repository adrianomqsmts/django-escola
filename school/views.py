from urllib import request
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from . import models
from . import forms

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    
    def get_template_names(self):
        if self.request.user.is_professor:
            return "dashboard_professor.html"
        else:
            return "dashboard_aluno.html"
        
class CourseListView(ListView):
    model = models.CourseClass
    context_object_name = 'classes'
    template_name = "course/course_list.html"
    
    def get_queryset(self):
        query = models.CourseClass.objects.filter(professor=self.request.user.professor)
        return query
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = models.CourseClass.objects.filter(professor=self.request.user.professor)
        context['Evaluations'] = models.Evaluation.objects.filter(professor=self.request.user.professor)
        return context
    
class EvaluationCreateView(CreateView):
    model = models.Evaluation
    form_class = forms.EvaluationCreationForm
    template_name = "Evaluation/Evaluation_create.html"
    success_url = reverse_lazy('course/course_list.html')
