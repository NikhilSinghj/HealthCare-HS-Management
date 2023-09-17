# Generated by Django 2.2 on 2023-09-17 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0002_auto_20230917_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
