# Generated by Django 4.0.3 on 2022-03-16 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_sala_horario_alter_disciplina_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professores', to='school.departamento'),
        ),
    ]
