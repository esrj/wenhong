# Generated by Django 4.2.1 on 2023-05-09 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_remove_lecture_title1_remove_lecture_title2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecture',
            old_name='content2',
            new_name='outline',
        ),
    ]