from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
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
    context_object_name = "classes"
    template_name = "course/course_list.html"

    def get_queryset(self):
        query = models.CourseClass.objects.filter(professor=self.request.user.professor)
        return query


class EvaluationCreateView(CreateView):
    model = models.Evaluation
    form_class = forms.EvaluationCreationForm
    template_name = "evaluation/evaluation_create.html"
    success_url = reverse_lazy("course_list")

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.course_class = models.CourseClass.objects.get(pk=self.kwargs["pk"])
        self.obj.professor = models.Professor.objects.get(
            id=self.request.user.professor.id
        )
        self.obj.save()
        return HttpResponseRedirect(reverse_lazy("course_list"))


class EvaluationUpdateView(UpdateView):
    model = models.Evaluation
    form_class = forms.EvaluationCreationForm
    template_name = "evaluation/evaluation_update.html"
    success_url = reverse_lazy("course_list")


class EvaluationDeleteView(DeleteView):
    model = models.Evaluation
    template_name = "evaluation/evaluation_delete.html"
    success_url = reverse_lazy("course_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class GradeEvaluationCreateView(TemplateView):
    template_name = "grades/grades_create.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject"] = models.CourseClass.objects.get(
            pk=self.kwargs["pk_subject"]
        )
        context["eval"] = models.Evaluation.objects.get(pk=self.kwargs["pk_eval"])
        context["students"] = context["subject"].students.all()
        return context


    def post(self, request, *args, **kwargs):
        i = 0
        for key, value in request.POST.items():
            if i == 0:
                i+=1
                continue
            try:
                grade_eval = models.GradeEvaluation()
                grade_eval.value = value
                grade_eval.student = models.Student.objects.get(registration=key)
                grade_eval.course_class = models.CourseClass.objects.get(pk=self.kwargs["pk_subject"])
                grade_eval.evaluation = models.Evaluation.objects.get(pk=self.kwargs["pk_eval"])
                grade_eval.save()
            except Exception as e:
                 return render(request, self.template_name, context={'error': e}) 
        return HttpResponseRedirect(reverse_lazy("course_list"))



