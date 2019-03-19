from django.db import models


class User(models.Model):
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

    def to_dict(self):
        return {
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'birth_year': self.birth_year,
            'birth_month': self.birth_month,
            'birth_day': self.birth_day,
            'avatar': self.avatar,
            'location': self.location,
        }