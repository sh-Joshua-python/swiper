import logging
from django.utils.deprecation import MiddlewareMixin
from libs.http import render_json

from user.models import User
from common import errors

err_log = logging.getLogger('err')

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
                err_log.error('%s:%s'%(errors.UserNotExist.code,errors.UserNotExist()))
                return render_json(code=errors.UserNotExist.code)
        else:
            err_log.error('%s:%s'%(errors.LoginReqired.code,errors.LoginReqired()))
            return render_json(code=errors.LogicError.code)


class LogicErrMiddleware(MiddlewareMixin):
    def process_exception(self,request,exception):
        if isinstance(exception,errors.LogicError):
            data = exception.data or str(exception)
            err_log.error('%s:%s'%(exception.code,data))
            return render_json(data=data,code=exception.code)