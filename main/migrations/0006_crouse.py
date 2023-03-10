# Generated by Django 4.0.5 on 2022-07-27 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_profile_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('photo', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='main.profile')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='main.profile')),
            ],
        ),
    ]
