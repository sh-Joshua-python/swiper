from django.db import models

from libs.cache import rds
from common.keys import MODEL_KEY

# class ModelMinxi:
def to_dict(self,*exclude):
    attr_dict = {}
    for field in self._meta.fields:
        name = field.attname
        if name not in exclude:
            attr_dict[name] = getattr(self,name)
    return attr_dict

def get(cls,*args,**kwargs):
    """
    Perform the query and return a single object matching the given
    keyword arguments.
    """
    #检查参数中是否有 主键
    if 'id' in kwargs or 'pk' in kwargs:
        #创建缓存 key
        pk = kwargs.get('id') or kwargs.get('pk')
        model_key = MODEL_KEY %(cls.__name__,pk)

        #先从缓存获取数据
        model_obj = rds.get(model_key)
        if model_obj is not None and isinstance(model_obj,cls):
            return model_obj

def get_or_create(cls,defaults=None,**kwargs):
    """
    Look up an object with the given kwargs, creating one if necessary.
    Return a tuple of (object, created), where created is a boolean
    specifying whether an object was created.
    """
    #检查参数中是否有主键
    if 'id' in kwargs or 'pk' in kwargs:
        #创建缓存 key
        pk = kwargs.get('id') or kwargs.get('pk')
        model_key = MODEL_KEY % (cls.__name___,pk)

        #先从缓存获取数据
        model_obj = rds.get(model_key)
        if model_obj is not None and isinstance(model_obj,cls):
            return model_obj,False

    #缓存中未取到，直接从数据库获取
    model_obj,created = cls.objects.get_or_create(defaults,**kwargs)
    #将数据库取出的数据写入缓存
    model_key = MODEL_KEY % (cls.__name__,model_obj.pk)
    rds.set(model_key,model_obj,ex=86400*7)
    return model_obj,created

def save(self,force_insert=False,force_update=False,using=None,update_fields=None):
    """
   Save the current instance. Override this in a subclass if you want to
   control the saving process.

   The 'force_insert' and 'force_update' parameters can be used to insist
   that the "save" must be an SQL insert or update (or equivalent for
   non-SQL backends), respectively. Normally, they should not be set.
   """
    #先执行原声的save 方法，将数据保存到数据库
    self._save(force_insert,force_update,using,update_fields)
    model_key = MODEL_KEY % (self.__class__.__name__,self.pk)
    rds.set(model_key,self,ex=86400*7)

def patch_model():
    '''通过 MonkeyPatch 的方式扩充 Model 的功能'''
    # 为 Model 添加 to_dict
    models.Model.to_dict = to_dict
    #为 Model添加 get 和 get_or_create 两个类方法
    models.Model.get=get
    models.Model.get_or_create = get_or_create
    #重新定义
    models.Model._save = models.Model.save
    models.Model.save = save

