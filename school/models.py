from django.db import models
from users.models import CustomUser
from django.db.models import Sum

class Professor(models.Model):
    registro = models.CharField(unique=True, null=True, max_length=45)
    escolaridade = models.CharField(max_length=150)
    salario = models.FloatField()
    user = models.OneToOneField(
        "users.CustomUser", on_delete=models.CASCADE, related_name="professor"
    )
    departamento = models.ForeignKey(
        "Departamento",
        on_delete=models.SET_NULL,
        related_name="professores",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return f"{self.registro}"


class Aluno(models.Model):

    matricula = models.CharField(max_length=45, unique=True)
    user = models.OneToOneField(
        "users.CustomUser", on_delete=models.CASCADE, related_name="alunos"
    )
    departamento = models.ForeignKey(
        "Departamento", on_delete=models.SET_NULL, null=True, related_name="alunos"
    )
    disciplinas = models.ManyToManyField("Disciplina", related_name='alunos')

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.matricula
    
    @classmethod
    def calcular_total_por_aluno(self, disciplina):
        alunos = self.objects.filter(disciplinas__id = disciplina.id)
        totais = []
        for aluno in alunos:
            totais.append({
                "aluno": aluno,
                "nota":aluno.notas.all().aggregate(Sum("valor"))
                })
        return totais


class Departamento(models.Model):

    nome = models.CharField(max_length=255, unique=True)
    coordenador = models.ForeignKey(
        "Professor",
        on_delete=models.SET_NULL,
        null=True,
        related_name="departamentos",
        blank=True,
    )

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nome


class Semestre(models.Model):

    nome = models.CharField(max_length=550, unique=True)

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"

    def __str__(self):
        return f"{self.nome}"


class Curso(models.Model):

    codigo = models.CharField(max_length=45, null=True)
    nome = models.CharField(max_length=255)
    creditos = models.IntegerField()

    departamento = models.ForeignKey(
        "Departamento", on_delete=models.SET_NULL, null=True, related_name="cursos"
    )
    
    prerequisitos = models.ManyToManyField("Curso")

    class Meta:
        verbose_name = "curso"
        verbose_name_plural = "cursos"
        unique_together = ("nome", "departamento")

    def __str__(self):
        return f"{self.codigo}"


class Sala(models.Model):
    porta = models.CharField(max_length=150)
    predio = models.CharField(max_length=150)
    capacidade = models.IntegerField(default=50)
    tem_projetor = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        unique_together = ["porta", "predio"]
        
    def __str__(self):
        return f"{self.predio}, sala: {self.porta}"


class Horario(models.Model):
    inicio = models.TimeField()
    termino = models.TimeField()
    sala = models.ForeignKey("Sala", on_delete=models.CASCADE, related_name="horarios")

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        unique_together = ["inicio", "sala"]

    def __str__(self):
        return f"{self.sala} : {self.inicio} - {self.termino}"


class Disciplina(models.Model):

    ano = models.DateField()
    eh_finalizada = models.BooleanField(default=False)
    professor = models.ForeignKey(
        "Professor", on_delete=models.SET_NULL, null=True, related_name="disciplinas"
    )
    curso = models.ForeignKey(
        "Curso", on_delete=models.SET_NULL, null=True, related_name="disciplinas"
    )
    semestre = models.ForeignKey(
        "Semestre", on_delete=models.SET_NULL, null=True, related_name="disciplinas"
    )
    horario = models.ForeignKey(
        "Horario", on_delete=models.SET_NULL, null=True, related_name="disciplinas"
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        unique_together = ("ano", "semestre", "horario")

    def __str__(self):
        return f"{self.curso.nome}"
    
    @classmethod
    def calcular_total_de_nota_distribuida_por_disciplina(self, professor):
        disciplinas = self.objects.filter(professor=professor).all()
        total = []
        for disciplina in disciplinas:
            total.append(
                {
                    'disciplina': disciplina,
                    'total': disciplina.avaliacoes.aggregate(Sum("valor"))  
                }
            )
        return total
    
    @classmethod
    def calcular_total_de_nota(self, disciplina):
        disciplina = self.objects.get(id=disciplina.id)
        total = disciplina.avaliacoes.exclude(tipo_avaliacao__nome='Extra').aggregate(Sum("valor"))
        return total
    

class TipoAvaliacao(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tipo de Avaliação"
        verbose_name_plural = "Tipos de Avaliações"

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    valor = models.FloatField()
    nota_eh_lancada = models.BooleanField(default=False)
    disciplina = models.ForeignKey(
        "Disciplina", on_delete=models.SET_NULL, null=True, related_name="avaliacoes"
    )
    tipo_avaliacao = models.ForeignKey(
        "TipoAvaliacao",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="avaliacoes",
    )

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ("disciplina", "nome")

    def __str__(self):
        return self.nome


class Nota(models.Model):
    valor = models.FloatField()
    aluno = models.ForeignKey("Aluno", on_delete=models.CASCADE, related_name="notas")
    avaliacao = models.ForeignKey(
        "Avaliacao", on_delete=models.CASCADE, related_name="notas"
    )

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        unique_together = ("avaliacao", "aluno")

    def __str__(self):
        return f"{self.valor}"
