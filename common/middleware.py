from django.utils.deprecation import MiddlewareMixin
from libs.http import render_json

from user.models import User
from common import errors


class AuthMiddleware(MiddlewareMixin):
    AUTH_URL_WHITE_LIST = [
        '/api/user/get_vcode/',
        '/api/user/check_vcode/',
    ]

    def process_request(self,requset):
        ''' '''
        if requset.path in self.AUTH_URL_WHITE_LIST:
            return

        ''' '''
        uid = requset.session.get('uid')
        if uid:
            try:
                requset.user = User.objects.get(id=uid)
                return
            except User.DoesNotExist:
                return render_json(code=errors.USER_NOT_EXIST)
        else:
            return render_json(code=errors.LOGIN_REQIRED)