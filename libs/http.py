import json

from django.conf import settings
from django.http import HttpResponse

from common.errors import OK


def render_json(data=None,code=OK):
    '''将结果渲染为一个惊悚数据的HttpResponse'''
    result = {
        'code':code,
        'data':data
    }

    #判断是否为DEBUG模式，返回值的展示
    if settings.DEBUG:
        json_result = json.dumps(result,ensure_ascii=False,indent=4,sort_keys=True)
    else:
        json_result = json.dumps(result,ensure_ascii=False,separators=(',',':'))

    return HttpResponse(json_result)