# _*_ encoding:utf-8 _*_

from django.http import HttpResponse
from rest_framework.views import APIView
import redis
import json

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
        # conn.publish("msgQueue", msg)
        return HttpResponse('{"status":"success"}', content_type="application/json")


@require_websocket
def echo(request):
    key_subscribe = "msgQueue"
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
        msg = None
        websocket = request.websocket
        # if count < 5:
        #     count += 1
        # else:
        #     websocket.send(json.dumps("当前连接人数已满，请稍后再试", ensure_ascii=False))
        #     websocket.close()
        try:
            websocket.send("连接成功")
            conn = redis.StrictRedis()
            # ps = conn.pubsub()
            # ps.subscribe(key_subscribe)
            # for item in ps.listen():
            #     if item['type'] == 'message':
            #         print item['data']
            #         websocket.send(item['data'])
            while True:
                # print conn.exists(key_subscribe)
                msg = conn.lpop(key_subscribe)
                # msg = conn.rpop(key_subscribe)
                if msg is not None:
                    websocket.send(msg)
        except BaseException as e:
            print e.message

