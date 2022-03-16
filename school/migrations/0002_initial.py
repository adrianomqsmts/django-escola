# Generated by Django 4.0.3 on 2022-03-16 01:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nota',
            name='aluno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notas', to='school.aluno'),
        ),
        migrations.AddField(
            model_name='nota',
            name='avaliacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notas', to='school.avaliacao'),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disciplina', to='school.curso'),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='periodo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disciplina', to='school.periodo'),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disciplina', to='school.professor'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='coordenador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departamentos', to='school.professor'),
        ),
        migrations.AddField(
            model_name='curso',
            name='departamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cursos', to='school.departamento'),
        ),
        migrations.AddField(
            model_name='curso',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cursos', to='school.professor'),
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='disciplina',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='avaliacoes', to='school.disciplina'),
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='tipo_avaliacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='avaliacoes', to='school.tipoavaliacao'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='departamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alunos', to='school.departamento'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='disciplinas',
            field=models.ManyToManyField(to='school.disciplina'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='alunos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='nota',
            unique_together={('avaliacao', 'aluno')},
        ),
        migrations.AlterUniqueTogether(
            name='disciplina',
            unique_together={('curso', 'ano', 'periodo')},
        ),
        migrations.AlterUniqueTogether(
            name='curso',
            unique_together={('nome', 'departamento')},
        ),
        migrations.AlterUniqueTogether(
            name='avaliacao',
            unique_together={('disciplina', 'nome')},
        ),
    ]
