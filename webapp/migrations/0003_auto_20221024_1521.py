# Generated by Django 2.2.5 on 2022-10-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20221024_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threatenhit',
            name='log_date',
            field=models.DateField(unique=True, verbose_name='日志产生时间'),
        ),
    ]
