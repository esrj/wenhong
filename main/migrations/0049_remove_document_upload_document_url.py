# Generated by Django 5.0.3 on 2024-05-06 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_remove_resource_file_resource_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='upload',
        ),
        migrations.AddField(
            model_name='document',
            name='url',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
