# Generated by Django 4.0.5 on 2022-09-26 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_rename_lecturer_lecture_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture', to='main.lecturer'),
        ),
    ]
