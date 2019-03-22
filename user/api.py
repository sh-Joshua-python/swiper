from django.core.cache import cache

from libs.http import render_json
from common import errors
from common import keys
from user import logics
# Create your views here.
from user.models import User
from user.forms import ProfileForm


def get_vcode(request):
    phonenum = request.POST.get('phonenum')
    if logics.is_phonenum(phonenum):
        #发送验证码
        logics.send_vcode(phonenum)
        # print('=========')
        return render_json()
    else:
        # print('====时报=====')
        return render_json(code=errors.PHONENUM_ERR)


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
                user = User.objects.get(phonenum=phonenum)
            except User.DoesNotExist:
                user = User.objects.create(phonenum=phonenum,nickname=phonenum)

            #在session中记录
            request.session['uid'] = user.id
            return render_json(data=user.to_dict())
        else:
            return render_json(code=errors.VCODE_ERR)

    else:
        return render_json(code=errors.PHONENUM_ERR)

def get_profile(request):
    ''''''
    profile_dict = request.user.profile.to_dict()
    return render_json(profile_dict)

def set_profile(request):
    ''''''
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = request.session['uid']
        profile.save()
        return render_json()
    else:
        return render_json(form.errors,errors.PROFILE_ERR)

def upload_avatar(request):
    '''上传个人形象图片'''
    avatar = request.FILES.get('avatar')
    print('-------FILES------------')
    logics.save_avator.delay(request.user,avatar)
    return render_json()
