# Generated by Django 4.0.5 on 2022-06-14 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
