# Generated by Django 4.2.1 on 2023-05-09 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_rename_content2_lecture_outline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecture',
            old_name='content1',
            new_name='introduce',
        ),
    ]
