# _*_ encoding:utf-8 _*_
from RedisSubscriber import RedisHelper

obj = RedisHelper()


def m_publish(msg):
    obj.public(msg)
