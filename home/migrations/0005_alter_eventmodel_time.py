# Generated by Django 4.2.6 on 2023-12-26 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_eventmodel_leader_eventmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='time',
            field=models.TimeField(),
        ),
    ]
