# Generated by Django 4.0.5 on 2022-07-04 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_teacher',
        ),
    ]