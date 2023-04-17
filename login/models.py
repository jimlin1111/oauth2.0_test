# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
from django.shortcuts import redirect


class SystemUserLoginInfo(models.Model):
    sn = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    access_token = models.CharField(max_length=512)
    token_type = models.CharField(max_length=32)
    refresh_token = models.CharField(max_length=64)
    at_expired = models.DateTimeField()
    scope = models.CharField(max_length=64)
    id_token = models.CharField(max_length=1024)
    user_pic = models.TextField()
    id_token_expired = models.DateTimeField()
    line_user_id = models.CharField(max_length=256)
    status = models.IntegerField()
    create_datetime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'system_user_login_info'

class SystemNotify(models.Model):
    sn = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    access_token = models.CharField(max_length=512)
    status = models.IntegerField()
    create_datetime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'system_notify'

class SystemCity(models.Model):
    sn = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = True
        db_table = 'system_city'

class SystemCityRefer(models.Model):
    sn = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    city_sn = models.IntegerField()
    create_datetime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'system_city_refer'

class LoginRequired():
    """
    檢查是否有登入，沒有則跳轉到login頁
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('auth:login'))
        return super().dispatch(request, *args, **kwargs)
