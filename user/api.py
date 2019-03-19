
from user import logics
from libs.http import render_json
from common import errors,keys
from django.core.cache import cache
# Create your views here.
from user.models import User


def get_vcode(request):
    phonenum = request.POST.get('phonenum')
    if logics.is_phonenum(phonenum):
        #发送验证码
        logics.send_vcode(phonenum)
        # print('=========')
        return render_json()
    else:
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