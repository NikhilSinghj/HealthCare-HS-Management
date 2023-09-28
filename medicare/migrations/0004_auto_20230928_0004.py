# Generated by Django 2.2 on 2023-09-28 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0003_auto_20230927_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='checkup_status',
            field=models.CharField(default='Not Checked', max_length=20),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='payment_status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='alcoholic',
            field=models.CharField(default='No', max_length=20),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='smoker',
            field=models.CharField(default='No', max_length=20),
        ),
    ]
