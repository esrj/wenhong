# Generated by Django 4.0.5 on 2022-07-24 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_contact_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='permission',
            field=models.IntegerField(default=0),
        ),
    ]
