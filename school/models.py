from django.db import models
from django.urls import reverse
from users.models import CustomUser


class Building(models.Model):
    name = models.CharField(max_length=255, unique=True)
    number = models.IntegerField()

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("building_detail", kwargs={"pk": self.pk})


class Department(models.Model):

    name = models.CharField(max_length=255, unique=True)
    building = models.ForeignKey(
        "Building",
        on_delete=models.SET_NULL,
        related_name="departments",
        blank=True,
        null=True,
    )
    budget = models.FloatField()
    coordinator = models.OneToOneField(
        "Professor",
        on_delete=models.SET_NULL,
        related_name="coordinator",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("department_detail", kwargs={"pk": self.pk})


class Professor(models.Model):
    schooling = models.CharField(max_length=45)
    salary = models.FloatField()
    user = models.OneToOneField(
        "users.CustomUser", on_delete=models.CASCADE, related_name="professor"
    )
    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="professors",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professors"

    def __str__(self):
        return f"{self.user.get_full_name()} | {self.department}"

    def get_absolute_url(self):
        return reverse("professor_detail", kwargs={"pk": self.pk})


class Student(models.Model):

    registration = models.CharField(max_length=45, unique=True)
    user = models.OneToOneField(
        "users.CustomUser", on_delete=models.CASCADE, related_name="student"
    )
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        related_name="students",
        blank=True,
        null=True,
    )
    courses_class = models.ManyToManyField(
        "CourseClass", related_name="students", blank=True
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse("student_detail", kwargs={"pk": self.pk})


class Course(models.Model):

    name = models.CharField(max_length=255, unique=True)
    total_credits = models.IntegerField()
    department = models.ForeignKey(
        "Department", on_delete=models.CASCADE, related_name="courses", default=None
    )
    prerequisites = models.ManyToManyField("Course", blank=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})


class CourseClass(models.Model):

    schedule = models.OneToOneField(
        "Schedule", on_delete=models.CASCADE, related_name="course_class"
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="course_classes"
    )
    professor = models.ForeignKey(
        "Professor",
        on_delete=models.CASCADE,
        related_name="course_classes",
        default=None,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Course Class"
        verbose_name_plural = "Course Classes"

    def __str__(self):
        return f"{self.course.name} | {self.schedule}"

    def get_absolute_url(self):
        return reverse("course_class_detail", kwargs={"pk": self.pk})


class Schedule(models.Model):
    classroom = models.ForeignKey(
        "Classroom", on_delete=models.CASCADE, related_name="schedules"
    )
    start_class = models.TimeField()
    finish_class = models.TimeField()

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        unique_together = ("classroom", "start_class")

    def __str__(self):
        return f"{self.classroom} : {self.start_class} - {self.finish_class}"

    def get_absolute_url(self):
        return reverse("schedule_detail", kwargs={"pk": self.pk})


class Classroom(models.Model):
    capacity = models.IntegerField()
    number = models.IntegerField()
    building = models.ForeignKey(
        "Building", on_delete=models.CASCADE, related_name="classrooms"
    )

    class Meta:
        verbose_name = "Classroom"
        verbose_name_plural = "Classrooms"
        unique_together = (
            "building",
            "number",
        )

    def __str__(self):
        return f"{self.building.name}, room: {self.number}"

    def get_absolute_url(self):
        return reverse("classroom_detail", kwargs={"pk": self.pk})


class TypeEvaluation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Type Evaluation"
        verbose_name_plural = "Type Evaluations"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("type_evaluation_detail", kwargs={"pk": self.pk})


class Evaluation(models.Model):
    course_class = models.ForeignKey(
        "CourseClass",
        on_delete=models.CASCADE,
        related_name="evaluations",
        default=None,
    )
    professor = models.ForeignKey(
        "Professor", on_delete=models.CASCADE, related_name="evaluations"
    )
    name = models.CharField(max_length=255)
    type_evaluation = models.ForeignKey(
        "TypeEvaluation",
        on_delete=models.SET_NULL,
        related_name="evaluations",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True)
    value = models.FloatField()
    # grade_value = models.FloatField()

    class Meta:
        verbose_name = "Evaluation"
        verbose_name_plural = "Evaluations"
        unique_together = ("course_class", "name")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("evaluation_detail", kwargs={"pk": self.pk})


class GradeEvaluation(models.Model):
    course_class = models.ForeignKey(
        "CourseClass",
        on_delete=models.SET_NULL,
        null=True,
        related_name="grade_evaluations",
    )
    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE, related_name="grade_evaluations"
    )
    evaluation = models.ForeignKey(
        "evaluation",
        on_delete=models.SET_NULL,
        related_name="grade_evaluations",
        null=True,
    )
    value = models.FloatField()

    class Meta:
        verbose_name = "Grade Evaluation"
        verbose_name_plural = "Grade Evaluations"
        unique_together = ("course_class", "student", "evaluation")

    def __str__(self):
        return f"{self.student.user.get_full_name()} | {self.course_class.course.name}"

    def get_absolute_url(self):
        return reverse("grade_evaluation_detail", kwargs={"pk": self.pk})
