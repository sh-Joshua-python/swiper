from urllib.parse import urljoin
from qiniu import Auth,put_file

from swiper import config


def qn_upload(filename,filepath):
    '''将文件上传至七牛云'''
    #构建鉴权对象
    qn = Auth(config.QN_ACCESS_KEY,config.QN_SECRET_KEY)
    #生产上传 Token,有效期为1小时
    token = qn.upload_token(config.QN_BUCKET,filename,3600)
    #上传文件
    ret,info = put_file(token,filename,filepath)

    if info.ok():
        url = urljoin(config.QN_BASEURL,filename)
        return True,url
    else:
        return False, ''