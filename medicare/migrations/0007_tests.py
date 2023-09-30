# Generated by Django 2.2 on 2023-09-29 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0006_auto_20230928_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=100, null=True, unique=True)),
                ('deleted_status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'avialable_tests',
            },
        ),
    ]
