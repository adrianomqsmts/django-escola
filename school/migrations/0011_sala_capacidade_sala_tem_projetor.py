# Generated by Django 4.0.3 on 2022-03-16 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0010_alter_sala_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='sala',
            name='capacidade',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='sala',
            name='tem_projetor',
            field=models.BooleanField(default=False),
        ),
    ]
