from django.db import models

from libs.orm import ModelMinxi
# from social.models import Swiped
from social.models import Friend
from vip.models import Vip

class User(models.Model,ModelMinxi):
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ('bj', '北京'),
        ('sh', '上海'),
        ('gz', '广州'),
        ('sz', '深圳'),
        ('wh', '武汉'),
        ('xa', '西安'),
        ('cd', '成都'),
    )
    phonenum = models.CharField(max_length=14, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, unique=True, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birth_year = models.IntegerField(default=2000, verbose_name='出生年')
    birth_month = models.IntegerField(default=1, verbose_name='出生月')
    birth_day = models.IntegerField(default=1, verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=8, choices=LOCATION, verbose_name='常居地')

    vip_id = models.IntegerField(verbose_name='用户对应的VIP ID')

    # def to_dict(self):
    #     return {
    #         'phonenum': self.phonenum,
    #         'nickname': self.nickname,
    #         'sex': self.sex,
    #         'birth_year': self.birth_year,
    #         'birth_month': self.birth_month,
    #         'birth_day': self.birth_day,
    #         'avatar': self.avatar,
    #         'location': self.location,
    #     }
    @property
    def profile(self):
        if not hasattr(self,'_profile'):
            self._profile,_ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    # @property
    # def swiped(self):
    #     if not hasattr(self,'_swiped'):
    #         self._swiped,_ = Swiped.objects.get_or_create(uid=self.id)
    #     return self._swiped
    @property
    def friends(self):
        '''所有的好友'''
        fid_list = Friend.friends_id_list(self.id)
        return User.objects.filter(id__in=fid_list)

    @property
    def vip(self):
        '''用户的VIP数据'''
        if not hasattr(self,'_vip'):
            self._vip = Vip.objects.get(self.vip_id)
        return self._vip


class Profile(models.Model,ModelMinxi):
    SEX = (
        ('male','男性'),
        ('female','女性'),
    )
    LOCATION = (
        ('bj', '北京'),
        ('sh', '上海'),
        ('gz', '广州'),
        ('sz', '深圳'),
        ('wh', '武汉'),
        ('xa', '西安'),
        ('cd', '成都'),
    )
    location = models.CharField(max_length=8, choices=LOCATION, verbose_name='目标城市')
    dating_sex = models.CharField(max_length=8, choices=SEX, verbose_name='匹配的性别')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')