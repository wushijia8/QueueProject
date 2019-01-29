# _*_ encoding:utf-8 _*_

from RedisSubscriber import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe()


def subscribe():
    msg = redis_sub.parse_response()
    return msg
