from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("disciplinas/list", views.DisciplinaListView.as_view(), name="list_disciplinas"),
    # path("student/list", views.CourseStudentListView.as_view(), name="course_list_student"),
    # # path("course/complete/<int:pk>", views.CourseCompletedUpdateView.as_view(), name="course_completed"),
    path("disciplina/<int:pk>/avalicao/create", views.AvaliacaoCreateView.as_view(), name="create_avaliacao"),
    path("avaliacao/<int:pk>/update", views.AvaliacaoUpdateView.as_view(), name="update_avaliacao"),
    path("avaliacao/<int:pk>/delete", views.AvaliacaoDeleteView.as_view(), name="delete_avaliacao"),
    path("disciplina/<int:pk_disciplina>/avaliacao/<int:pk_avaliacao>/notas/create", views.NotasCreateView.as_view(), name="larcar_notas"),
    # path("course/<int:pk_subject>/student/<int:pk_std>/grades/list", views.StudentGradesListView.as_view(), name="grades_student_list"),
    # path("grades/<int:pk>", views.GradesUpdateView.as_view(), name="grades_update"),
]
