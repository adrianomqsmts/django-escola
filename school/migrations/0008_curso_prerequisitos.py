# Generated by Django 4.0.3 on 2022-03-16 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_alter_departamento_coordenador'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='prerequisitos',
            field=models.ManyToManyField(to='school.curso'),
        ),
    ]
