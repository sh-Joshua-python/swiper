import logging
from django.core.cache import cache

from libs.http import render_json
from common import errors
from common import keys
from user import logics
# Create your views here.
from user.models import User
from user.forms import ProfileForm

inf_log = logging.getLogger('inf')

def get_vcode(request):
    phonenum = request.POST.get('phonenum')
    if logics.is_phonenum(phonenum):
        #发送验证码
        logics.send_vcode(phonenum)
        # print('=========')
        return render_json()
    else:
        # print('====时报=====')
        raise errors.PhonenumErr


def check_vcode(request):
    '''Review vcode'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    #检查手机号是否合法
    if logics.is_phonenum(phonenum):
        #从缓存中获取验证码
        cached_vcode = cache.get(keys.VCODE_KEY % phonenum)
        if cached_vcode == vcode:
            try:
                user = User.get(phonenum=phonenum)
            except User.DoesNotExist:
                user = User.objects.create(phonenum=phonenum,nickname=phonenum)

            #在session中记录
            request.session['uid'] = user.id
            inf_log.info('Login:%s %s'%(user.id,user.nickname))
            return render_json(data=user.to_dict())
        else:
            raise errors.VcodeErr

    else:
        raise errors.PhonenumErr

def get_profile(request):
    '''获取用户个人资料'''
    key = keys.PROFILE_KEY % request.user.id
    profile_dict = cache.get(key)
    #从缓存中获取
    if profile_dict is None:
        profile_dict = request.user.profile.to_dict()
        #写入缓存
        cache.set(key,profile_dict,3600)
    return render_json(profile_dict)

def set_profile(request):
    '''设置用户个人资料'''
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = request.session['uid']
        profile.save()

        #修改缓存
        key = keys.PROFILE_KEY % request.user.id
        cache.set(key,profile.to_dict(),3600)
        return render_json()
    else:
        raise errors.ProfileErr(form.errors)

def upload_avatar(request):
    '''上传个人形象图片'''
    avatar = request.FILES.get('avatar')
    print('-------FILES------------')
    logics.save_avator.delay(request.user,avatar)
    return render_json()
