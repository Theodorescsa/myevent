# Generated by Django 4.2.6 on 2023-12-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_eventmodel_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='deadline',
            field=models.DateField(null=True),
        ),
    ]