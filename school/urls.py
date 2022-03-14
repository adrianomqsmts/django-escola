from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("course/list", views.CourseListView.as_view(), name="course_list"),
    path("Evaluation/create", views.EvaluationCreateView.as_view(), name="Evaluation_create"),
]
