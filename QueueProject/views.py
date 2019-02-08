# _*_ encoding:utf-8 _*_

from django.http import HttpResponse
from rest_framework.views import APIView
import redis
import json
import time

from dwebsocket import require_websocket

from publish import m_publish

count = 0


class Receiver(APIView):
    def post(self, request):
        num1 = request.data[u"num1"]
        num2 = request.data[u"num2"]
        return HttpResponse('{"status":"success"}', content_type='application/json')


class Publish(APIView):
    def post(self, request):
        msg = request.data[u"msg"]
        conn = redis.StrictRedis()
        conn.lpush("msgQueue", msg)
        return HttpResponse('{"status":"success"}', content_type="application/json")


@require_websocket
def echo(request):
    key_subscribe = 'fm104.5'
    global count
    if not request.is_websocket():
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except BaseException as e:
            print e.message
            return HttpResponse(e.message)
    else:
        conn = None
        websocket = request.websocket
        if count < 5:
            count += 1
        else:
            websocket.send(json.dumps("当前连接人数已满，请稍后再试", ensure_ascii=False))
            websocket.close()
        try:
            websocket.send("连接成功")
            conn = redis.StrictRedis()
            while True:
                msg = conn.brpop("msgQueue")[1]
                if msg is None:
                    continue
                websocket.send(msg)
        except BaseException as e:
            print e.message

