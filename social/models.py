from django.db import models

# Create your models here.

# class Swiped(models.Model):
#     MARK = (
#         ('left','small'),
#         ('right','big'),
#         ('top','huge')
#     )
#     uid = models.IntegerField(verbose_name='用户自身id')
#     sid = models.IntegerField(verbose_name='被滑陌生人的id')
#     mark = models.CharField(max_length=8,choices=MARK,verbose_name='滑动类型')
#     time = models.TimeField(auto_now_add=True,verbose_name='滑动的时间')
#
# class Friend(models.Model):
#     uid = models.IntegerField(verbose_name='好友ID')