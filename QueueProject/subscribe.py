# _*_ encoding:utf-8 _*_

import redis


def subscribe():
    conn = redis.StrictRedis()
    msg = conn.brpop("msgQueue")[1]
    print msg


# subscribe()
