# Generated by Django 2.2 on 2023-09-28 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0004_auto_20230928_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalhistory',
            name='symptoms',
        ),
        migrations.AddField(
            model_name='appointment',
            name='symptoms',
            field=models.CharField(max_length=100, null=True),
        ),
    ]