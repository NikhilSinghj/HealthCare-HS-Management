# Generated by Django 2.2 on 2023-09-20 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0004_auto_20230919_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leftpanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('panel', models.CharField(max_length=50)),
                ('dashboard', models.CharField(max_length=30)),
                ('deleted_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='prescription',
            name='prescription_date',
            field=models.DateField(auto_now=True),
        ),
    ]