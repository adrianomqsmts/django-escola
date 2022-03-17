from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from . import models
from . import forms
from django.contrib import messages


from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


class IndexView(TemplateView):
    template_name = "index.html"


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_template_names(self):
        if self.request.user.is_professor:
            return "dashboard_professor.html"
        else:
            return "dashboard_aluno.html"


class AlunoDisciplinasListView(ListView):
    model = models.Disciplina
    context_object_name = "disciplinas"
    template_name = "disciplina/list_aluno.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno = self.request.user.aluno
        context["notas"] = []
        notas = aluno.notas.all()
        for nota in notas:
            if nota.valor >= (0.6 * nota.avaliacao.valor):
                context["notas"].append({"nota": nota, "alert": "success"})
            elif nota.valor >= (0.4 * nota.avaliacao.valor):
                context["notas"].append({"nota": nota, "alert": "warning"})
            else:
                context["notas"].append({"nota": nota, "alert": "danger"})

        nota_disciplinas = models.Disciplina.calcular_total_do_aluno_por_disciplina(
            aluno
        )
        context["nota_disciplinas"] = []
        for nota_disciplina in nota_disciplinas:
            if nota_disciplina["total"] != None:
                if nota_disciplina["total"] >= 60:
                    context["nota_disciplinas"].append(
                        {"total": nota_disciplina["total"], "disciplina": nota_disciplina["disciplina"], "alert": "success"}
                    )
                elif nota_disciplina["total"] >= 40:
                    context["nota_disciplinas"].append(
                        {"total": nota_disciplina["total"], "disciplina": nota_disciplina["disciplina"], "alert": "warning"}
                    )
                else:
                    context["nota_disciplinas"].append(
                        {"total": nota_disciplina["total"], "disciplina": nota_disciplina["disciplina"], "alert": "danger"}
                    )
            else:
                context["nota_disciplinas"].append({"total": 0.0, "disciplina": nota_disciplina["disciplina"], "alert": "danger"})

        return context

    def get_queryset(self):
        query = models.Disciplina.objects.filter(alunos=self.request.user.aluno)
        return query


class DisciplinaListView(ListView):
    model = models.Disciplina
    context_object_name = "disciplinas"
    template_name = "disciplina/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "total_por_disciplina"
        ] = models.Disciplina.calcular_total_de_nota_distribuida_por_disciplina(
            self.request.user.professor
        )
        return context

    def get_queryset(self):
        query = models.Disciplina.objects.filter(professor=self.request.user.professor)
        return query


class AvaliacaoCreateView(CreateView):
    model = models.Avaliacao
    form_class = forms.AvaliacaoCreationForm
    template_name = "avaliacao/create.html"
    success_url = reverse_lazy("list_disciplinas")

    def form_valid(self, form):
        avaliacao = form.save(commit=False)
        avaliacao.disciplina = models.Disciplina.objects.get(pk=self.kwargs["pk"])
        avaliacao.professor = models.Professor.objects.get(
            id=self.request.user.professor.id
        )
        disciplina_total = models.Disciplina.calcular_total_de_nota(
            avaliacao.disciplina,
        )["valor__sum"]
        if disciplina_total:
            total = avaliacao.valor + disciplina_total
        else:
            total = avaliacao.valor
        if total > 100:
            context = self.get_context_data()
            messages.warning(
                self.request,
                "Valor da Avalição faz com que o semestre supere 100 pontos.",
            )
            return render(self.request, self.template_name, context=context)
        try:
            search = models.Avaliacao.objects.get(nome=avaliacao.nome)
        except Exception as e:
            search = False
        if search:
            messages.warning(
                self.request,
                "Ops! A avaliação com este nome já existe dentro da disciplina. Tente novamente.",
            )
            form.add_error("nome", "A avaliação já existe...")
            context = self.get_context_data()
            return render(self.request, self.template_name, context=context)
        avaliacao.save()
        return HttpResponseRedirect(reverse_lazy("list_disciplinas"))


class AvaliacaoUpdateView(UpdateView):
    model = models.Avaliacao
    form_class = forms.AvaliacaoCreationForm
    template_name = "avaliacao/update.html"
    success_url = reverse_lazy("list_disciplinas")


class AvaliacaoDeleteView(DeleteView):
    model = models.Avaliacao
    template_name = "avalicao/delete.html"
    success_url = reverse_lazy("list_disciplinas")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class NotasCreateView(TemplateView):
    template_name = "notas/create.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disciplina"] = models.Disciplina.objects.get(
            pk=self.kwargs["pk_disciplina"]
        )
        context["avaliacao"] = models.Avaliacao.objects.get(
            pk=self.kwargs["pk_avaliacao"]
        )
        context["alunos"] = context["disciplina"].alunos.all()
        return context

    def post(self, request, *args, **kwargs):
        i = 0
        notas = []
        for key, value in request.POST.items():
            if i == 0:
                i += 1
                continue
            avaliacao = models.Avaliacao.objects.get(pk=self.kwargs["pk_avaliacao"])
            try:
                float(value)
            except:
                messages.warning(
                    self.request,
                    f"Lamento, a nota do aluno com matricula {key} não é um valor válido",
                )
                return render(
                    request, self.template_name, context=self.get_context_data()
                )
            if (float(value) > avaliacao.valor) or (float(value) <= 0):
                messages.warning(
                    self.request,
                    f"Lamento, a nota do aluno com matricula {key} supera a nota da avaliacao",
                )
                return render(
                    request, self.template_name, context=self.get_context_data()
                )
            notas.append(
                models.Nota(
                    valor=value,
                    aluno=models.Aluno.objects.get(matricula=key),
                    avaliacao=avaliacao,
                )
            )
            for nota in notas:
                nota.save()
            avaliacao = models.Avaliacao.objects.get(pk=self.kwargs["pk_avaliacao"])
            avaliacao.nota_eh_lancada = True
            avaliacao.save()
        return HttpResponseRedirect(reverse_lazy("list_disciplinas"))


class DisciplinaNotaListView(ListView):
    model = models.Aluno
    context_object_name = "alunos"
    template_name = "aluno/list_nota_disciplina.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disciplina"] = models.Disciplina.objects.get(
            id=self.kwargs["pk_disciplina"]
        )
        context["notas"] = models.Aluno.calcular_total_por_aluno(context["disciplina"])
        return context

    def get_queryset(self, *args, **kwargs):
        return models.Aluno.objects.filter(
            departamento__cursos__disciplinas__id=self.kwargs["pk_disciplina"]
        )


class AlunoNotaListView(ListView):
    context_object_name = "notas"
    template_name = "notas/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aluno"] = models.Aluno.objects.get(id=self.kwargs["pk_aluno"])
        context["disciplina"] = models.Disciplina.objects.get(
            id=self.kwargs["pk_disciplina"]
        )
        return context

    def post(self, request, *args, **kwargs):
        i = 0
        for key, value in request.POST.items():
            if i == 0:
                i += 1
                continue
            nota = models.Nota.objects.get(pk=key)
            nota.valor = float(request.POST.get(str(key)))
            if (nota.valor) <= 0 or (nota.avaliacao.valor < nota.valor):
                messages.warning(request, f"Lamento, a nota supera a nota da avaliacao")
                return redirect(
                    "list_aluno_notas",
                    pk_disciplina=self.kwargs["pk_disciplina"],
                    pk_aluno=self.kwargs["pk_aluno"],
                )
            nota.save()
            messages.success(request, f"Nota atualizada com sucesso.")
        return redirect(
            "list_aluno_notas",
            pk_disciplina=self.kwargs["pk_disciplina"],
            pk_aluno=self.kwargs["pk_aluno"],
        )

    def get_queryset(self, *args, **kwargs):
        query = models.Nota.objects.filter(
            aluno__id=self.kwargs["pk_aluno"],
            avaliacao__disciplina=self.kwargs["pk_disciplina"],
        )
        return query


class AvaliacaoDetailView(DetailView):
    model = models.Avaliacao
    context_object_name = 'avaliacao'
    template_name = "avaliacao/detail.html"
