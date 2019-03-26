from common import errors

def need_perm(perm_name):
    '''权限检查装饰器'''
    def deco(view_func):
        def wrapper(request):
            if request.user.vip.has_perm(perm_name):
                return view_func
            else:
                raise errors.PermissionRequired
        return wrapper
    return deco