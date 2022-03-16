from django.urls import path
from . import views

urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    # path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    # path("course/list", views.CourseListView.as_view(), name="course_list"),
    # path("student/list", views.CourseStudentListView.as_view(), name="course_list_student"),
    # # path("course/complete/<int:pk>", views.CourseCompletedUpdateView.as_view(), name="course_completed"),
    # path("course/<int:pk>/evaluation/create", views.EvaluationCreateView.as_view(), name="evaluation_create"),
    # path("evaluation/<int:pk>/update", views.EvaluationUpdateView.as_view(), name="evaluation_update"),
    # path("evaluation/<int:pk>/delete", views.EvaluationDeleteView.as_view(), name="evaluation_delete"),
    # path("course/<int:pk_subject>/evaluation/<int:pk_eval>/grades/create", views.GradeEvaluationCreateView.as_view(), name="grades_create"),
    # path("course/<int:pk_subject>/student/<int:pk_std>/grades/list", views.StudentGradesListView.as_view(), name="grades_student_list"),
    # path("grades/<int:pk>", views.GradesUpdateView.as_view(), name="grades_update"),
]
