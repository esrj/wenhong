# Generated by Django 4.2.1 on 2023-05-09 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_lecture_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='title1',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='title2',
        ),
    ]