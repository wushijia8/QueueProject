# _*_ encoding:utf-8 _*_

from django.http import HttpResponse
from rest_framework.views import APIView
import time

from dwebsocket import require_websocket
import pika

from .rbSend import send

count = 0


class Receiver(APIView):
    def post(self, request):
        num1 = request.data[u"num1"]
        num2 = request.data[u"num2"]
        return HttpResponse('{"status":"success"}', content_type='application/json')


class Publish(APIView):
    def post(self, request):
        msg = request.data[u"msg"]
        msg += " " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        send(msg)
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
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            ch = ''
            method = ''
            lis = []

            def callback(ch, method, properties, body):
                ch = ch
                method = method
                print body
                websocket.send(body)

            channel.basic_consume(callback, queue='task_queues', no_ack=True)
            channel.start_consuming()
            ch.basic_qos(prefetch_count=1)
            connection.close()
        except BaseException as e:
            print e

