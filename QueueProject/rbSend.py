# _*_ encoding:utf-8 _*_
"""
@Time:2019-02-13 13:53:32
@Author:jaris
"""

import pika
import time, sys


def send(msg):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = conn.channel()

    channel.queue_declare(queue='task_queues', durable=True)
    channel.basic_publish(exchange='',
                          routing_key='task_queues',
                          body=msg,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

