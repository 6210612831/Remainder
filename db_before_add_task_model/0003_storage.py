# Generated by Django 4.0.5 on 2022-07-11 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('path', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]