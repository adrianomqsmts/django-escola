# Generated by Django 4.0.3 on 2022-03-13 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_alter_building_name_alter_course_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('classroom', 'start_class')},
        ),
    ]