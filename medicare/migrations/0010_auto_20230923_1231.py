# Generated by Django 2.2 on 2023-09-23 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0009_auto_20230922_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='leftpanel',
            name='icons',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leftpanel',
            name='state',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AlterModelTable(
            name='leftpanel',
            table='Leftpanel',
        ),
    ]