import random
import re
import os
import requests

from django.conf import settings
from django.core.cache import cache
from common import constant,keys
from libs.qncloud import qn_upload
from worker import celery_app
from swiper import config


def is_phonenum(phonenum):
    '''检查手机号是否正常'''
    # if re.match(constant.PHONENUM_REP,phonenum):
    if re.match(r'^1[3456789]\d{9}$',phonenum):
        return True
    else:
        return False

def get_random_code(length=4):
    '''产生一个指定长度的随机码'''
    rand_num = random.randrange(constant.ZERO,constant.TEN**length)
    template = '%%0%sd' % length
    vcode = template % rand_num
    return vcode


def sent_sms(phonenum, vcode):
    '''发送短信'''
    args = config.YZX_SMS_ARGS.copy() #原型模式
    args['param'] = vcode
    args['mobile'] = phonenum
    response = requests.post(config.YZX_SMS_API,json=args)
    return response


def send_vcode(phonenum):
    '''发送验证码'''
    vcode = get_random_code(4) #产生4位随机验证码
    print('===============',vcode)#测试用
    response = sent_sms(phonenum,vcode)#发送验证码

    #检查发送状态是否成功
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == '000000':
            key = keys.VCODE_KEY % phonenum
            cache.set(key,vcode,180)
            return True
    return False

def save_upload_file(uid,upload_file):
    '''保存上传文件'''
    filename = 'Avator-%s' % uid
    fullpath = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,filename)
    print('------图片存储--------')
    with open(fullpath,'wb') as fp:
        for chunk in upload_file.chunks():
            fp.write(chunk)
    return fullpath,filename


@celery_app.task
def save_avator(user,avator_file):
    '''上传用户头像'''
    #将文件保存到本地
    fullpath,filename = save_upload_file(user.id,avator_file)
    #将文件上传至七牛云
    _,avatar_url = qn_upload(filename,fullpath)
    #将URL保存到 UserModel
    user.avatar = avatar_url
    user.save()
