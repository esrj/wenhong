# Generated by Django 4.0.5 on 2022-07-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_profile_is_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_contact', models.BooleanField(default=False)),
                ('is_sign', models.BooleanField(default=False)),
            ],
        ),
    ]
