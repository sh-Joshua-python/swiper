# from django.db import models

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

from django.db import models
from django.db.models import Q

from common import errors


class Swiped(models.Model):
    '''活动记录'''
    STYPE = (
        ('dislike', '左滑'),
        ('like', '右滑'),
        ('superlike', '上滑'),
    )
    uid = models.IntegerField(verbose_name='滑动者的 UID')
    sid = models.IntegerField(verbose_name='被滑动者的 UID')
    stype = models.CharField(max_length=10, choices=STYPE, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True)

    @classmethod
    def swipe(cls, uid, sid, stype):
        '''添加一条滑动记录'''
        if stype not in ['dislike', 'like', 'superlike']:
            raise errors.StypeErr

        # 使用 get_or_create，避免重复创建滑动记录
        swiped, _ = cls.objects.get_or_create(uid=uid, sid=sid, stype=stype)
        return swiped

    @classmethod
    def is_liked(cls, uid, sid):
        '''检查是否喜欢过某人'''
        return cls.objects.filter(uid=uid, sid=sid, stype__in=['like', 'superlike']).exists()

    @classmethod
    def who_liked_me(cls, uid):
        '''喜欢过我的人的 UID'''
        liked_me = cls.objects.filter(sid=uid, stype__in=['like', 'superlike'])
        return liked_me.values_list('uid', flat=True)


class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='好友ID 1')
    uid2 = models.IntegerField(verbose_name='好友ID 2')

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''建立好友关系'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        friends, _ = cls.objects.get_or_create(uid1=uid1, uid2=uid2)
        return friends

    @classmethod
    def break_off(cls, uid1, uid2):
        '''断交'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def is_friends(cls, uid1, uid2):
        '''检查两个人是否是好友关系'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()

    @classmethod
    def friends_id_list(cls, uid):
        '''获取所有的好友 ID'''
        condition = Q(uid1=uid) | Q(uid2=uid)
        all_friends = cls.objects.filter(condition)
        fid_list = []
        for friend in all_friends:
            fid = friend.uid1 if friend.uid2 == uid else friend.uid2
            fid_list.append(fid)
        return fid_list
