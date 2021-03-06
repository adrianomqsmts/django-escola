# Generated by Django 4.0.3 on 2022-03-16 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_curso_prerequisitos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Periodo',
            new_name='Semestre',
        ),
        migrations.AlterModelOptions(
            name='semestre',
            options={'verbose_name': 'Semestre', 'verbose_name_plural': 'Semestres'},
        ),
        migrations.RenameField(
            model_name='disciplina',
            old_name='periodo',
            new_name='semestre',
        ),
        migrations.AlterUniqueTogether(
            name='disciplina',
            unique_together={('curso', 'ano', 'semestre', 'horario')},
        ),
    ]
