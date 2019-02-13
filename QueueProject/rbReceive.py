# _*_ encoding:utf-8 _*_
"""
@Time:2019-02-13 16:23:14
@Author:jaris
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
ch = ''
method = ''
lis = []


def callback(ch, method, properties, body):
    ch = ch
    method = method
    print body


channel.basic_consume(callback, queue='task_queues', no_ack=True)
channel.start_consuming()
ch.basic_qos(prefetch_count=1)
connection.close()
