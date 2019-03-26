from libs.http import render_json
from vip.models import Vip


def show_vip(request):
    '''VIP 和权限展示'''
    vip_info_list = []
    for vip in Vip.objects.all():
        vip_info = vip.to_dict('id')
        vip_info['perms'] = []
        for perm in vip.perms():
            perm_info = perm.to_dict('id')
            vip_info['perms'].append(perm_info)
        vip_info_list.append(vip_info)
    return render_json(vip_info_list)
