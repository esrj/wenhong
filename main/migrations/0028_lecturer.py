# Generated by Django 4.0.5 on 2022-09-26 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_resource_lecture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
    ]
