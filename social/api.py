# Create your views here.
import logging
from libs.http import render_json
from social import logics
from social.models import Swiped
from user.models import User
from vip.logics import need_perm

inf_log = logging.getLogger('inf')

def get_rmcds(request):
    '''获取推荐列表'''
    users = logics.get_rcmd_list(request.user,20)
    rcmd_data = [user.to_dict() for user in users]
    return render_json(rcmd_data)

def dislike(request):
    sid = int(request.POST.get('sid'))
    Swiped.swipe(request.user.id,sid,'dislike')
    inf_log.info('%s dislike %s'%(request.user.id,sid))
    return render_json()

def like(request):
    sid = int(request.POST.get('sid'))
    matched = logics.like_someone(request.user,sid)
    inf_log.info('%s like %s'%(request.user.id,sid))
    return render_json({'is_matched':matched})

@need_perm('superlike')
def superlike(request):
    sid = int(request.POST.get('sid'))
    matched = logics.superlike_someone(request.user,sid)
    inf_log.info('%s superlike %s'%(request.user.id,sid))
    return render_json({'is_matched':matched})

def friends(request):
    friends_data = [friend.to_dict() for friend in request.user.friends]
    return render_json(friends_data)

@need_perm('rewind')
def rewind(request):
    '''反悔'''
    logics.rewind(request.user)
    return render_json()

@need_perm('show_liked_me')
def show_liked_me(request):
    '''查看喜欢过我的人'''
    liked_me_uid_list = Swiped.who_liked_me(request.user.id)
    liked_me_users = User.objects.filter(id__in=liked_me_uid_list)
    result =[user.to_dict() for user in liked_me_users]
    return render_json(result)