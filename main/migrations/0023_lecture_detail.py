# Generated by Django 4.0.5 on 2022-09-25 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_remove_more_page_delete_detail_delete_more_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('title1', models.TextField()),
                ('content1', models.TextField()),
                ('title2', models.TextField()),
                ('content2', models.TextField()),
                ('text', models.TextField()),
                ('fee', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.lecture')),
            ],
        ),
    ]