from lib import broker

__author__ = 'ehonlia'

import pika
import base64
import urllib
import urllib2
import json

from constants import METADATA


def __upload(body, type):
    message = json.loads(body)

    data = urllib.urlencode({
        'data': message[METADATA],
        'baseURI': 'http://iot.iot/streams/'
    })
    url = 'http://192.121.150.101:3020/servlets/uploadData'
    username = 'admin'
    password = 's3cret'

    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    req = urllib2.Request(url, data)
    req.add_header("Authorization", "Basic %s" % base64string)
    urllib2.urlopen(req)


def __callback_stream(ch, method, properties, body):
    __upload(body, 'streams')


def __callback_virtual_stream(ch, method, properties, body):
    __upload(body, 'virtual_streams')


def subscribe_to_stream_update():
    connect = pika.BlockingConnection(pika.ConnectionParameters(host=broker.HOST))
    channel = connect.channel()

    channel.exchange_declare(exchange=broker.SEMANTIC_STREAM_EXCHANGE, type=broker.EXCHANGE_TYPE)

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=broker.SEMANTIC_STREAM_EXCHANGE, queue=queue_name,
                       routing_key=broker.SEMANTIC_STREAM_ROUTING_KEY)

    channel.basic_consume(__callback_stream, queue=queue_name, no_ack=True)
    channel.start_consuming()


def subscribe_to_virtual_stream_update():
    connect = pika.BlockingConnection(pika.ConnectionParameters(host=broker.HOST))
    channel = connect.channel()

    channel.exchange_declare(exchange=broker.SEMANTIC_VIRTUAL_STREAM_EXCHANGE, type=broker.EXCHANGE_TYPE)

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=broker.SEMANTIC_VIRTUAL_STREAM_EXCHANGE, queue=queue_name,
                       routing_key=broker.SEMANTIC_VIRTUAL_STREAM_ROUTING_KEY)

    channel.basic_consume(__callback_virtual_stream, queue=queue_name, no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    subscribe_to_stream_update()
