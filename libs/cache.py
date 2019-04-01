from pickle import dumps,loads
from redis import Redis as _Redis

from swiper import settings

class Redis(_Redis):
    def get(self,name):
        pickled = super().get(name)
        try:
            return loads(pickled)
        except TypeError:
            return pickled

    def set(self,name,value,ex=None,px=None,nx=False,xx=False):
        pickled = dumps(value,-1)
        return super().set(name,pickled,ex,px,nx,xx)

rds = Redis(**settings.REDIS)