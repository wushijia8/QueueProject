# _*_ encoding:utf-8 _*_
import redis
import time


def m_publish(msg):
    conn = redis.StrictRedis()
    print msg
    conn.lpush("msgQueue", msg)


# m_publish("publish msg " + str(time.time()))
