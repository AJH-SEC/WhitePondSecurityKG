from django.db import models


# 用户表
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, verbose_name="用户名")
    gender = models.IntegerField(verbose_name="性别：1-男 2-女")
    password = models.CharField(max_length=256, null=True, verbose_name="密码")


class ThreatenHit(models.Model):
    id = models.AutoField(primary_key=True)
    log_date = models.DateField(verbose_name="日志产生时间", unique=True)
    hit_count = models.IntegerField(verbose_name="命中数量")
