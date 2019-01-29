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
        print msg
        m_publish(msg)
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
        redis_cli = None
        redis_pubsub = None
        websocket = request.websocket
        if count < 1:
            count += 1
        else:
            websocket.send(json.dumps("当前连接人数已满，请稍后再试", ensure_ascii=False))
            websocket.close()
        try:
            redis_cli = redis.Redis(host='127.0.0.1')
            redis_pubsub = redis_cli.pubsub()
            redis_pubsub.subscribe(key_subscribe)

            while True:
                message = redis_pubsub.parse_response()
                print "message", message
                websocket.send(json.dumps(str(message[-1]) + "：" + str(time.time()), ensure_ascii=False))
                # ws_msg = websocket.read()
                # sub_msg = redis_pubsub.get_message()
                # if ws_msg:
                #     msg = json.loads(ws_msg)
                #     msg['date'] = time.asctime(time.localtime(time.time()))
                #     redis_cli.pubsub(key_subscribe, json.dumps(msg))
                #
                # if sub_msg and sub_msg['type'] == 'message':
                #     message = json.loads(sub_msg['date'])
                #     message['code'] = 200
                #     websocket.send(json.dumps(message))
        except BaseException as e:
            print e.message

