# Generated by Django 2.2.5 on 2022-10-24 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threatenhit',
            name='log_date',
            field=models.DateField(auto_now_add=True, verbose_name='日志产生时间'),
        ),
    ]
