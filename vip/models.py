from django.db import models
# from libs.orm import ModelMinxi
# Create your models here.

class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=10,unique=True,verbose_name='Vip的名字')
    level = models.IntegerField(verbose_name='会员等级')
    price = models.FloatField(verbose_name='会员的价格')

    class Meta:
        '''默认以某个字段排序'''
        ordering = ['level']

    def perms(self):
        '''查看当前会员拥有的所有权限'''
        perm_id_list = VipPermRelation.objects.filter(vip_id=self.id).values_list('perm_id',flat=True)
        return Permission.objects.filter(id__in=perm_id_list)

    def has_perm(self,perm_name):
        for perm in self.perms():
            if perm.name == perm_name:
                return True
        return False


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=10,unique=True,verbose_name='权限名称')
    description = models.TextField(verbose_name='权限详情介绍')


class VipPermRelation(models.Model):
    vip_id = models.IntegerField(verbose_name='Vip的ID')
    perm_id = models.IntegerField(verbose_name='Permission的ID')