__author__ = 'ehonlia'

import pika
import json
import logging

import semantics
from constants import ID, METADATA

HOST = 'honnix-ws'
EXCHANGE_TYPE = 'topic'
STREAM_EXCHANGE = 'topic_stream'
VIRTUAL_STREAM_EXCHANGE = 'topic_virtual_stream'
SEMANTIC_STREAM_EXCHANGE = 'topic_semantic_stream'
SEMANTIC_VIRTUAL_STREAM_EXCHANGE = 'topic_semantic_virtual_stream'
STREAM_ROUTING_KEY = 'stream'
VIRTUAL_STREAM_ROUTING_KEY = 'virtual_stream'
SEMANTIC_STREAM_ROUTING_KEY = 'semantic_stream'
SEMANTIC_VIRTUAL_STREAM_ROUTING_KEY = 'semantic_virtual_stream'


def __callback_stream(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)

    stream_id, semantic_stream = semantics.semantic_stream(json.loads(body))
    print semantic_stream

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=SEMANTIC_STREAM_EXCHANGE, type=EXCHANGE_TYPE)
    channel.basic_publish(exchange=SEMANTIC_STREAM_EXCHANGE, routing_key=SEMANTIC_STREAM_ROUTING_KEY,
                          body=json.dumps({ID: stream_id, METADATA: semantic_stream}))
    connection.close()


def __callback_virtual_stream(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)

    stream_id, semantic_virtual_stream = semantics.semantic_virtual_stream(json.loads(body))

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=SEMANTIC_VIRTUAL_STREAM_EXCHANGE, type=EXCHANGE_TYPE)
    channel.basic_publish(exchange=SEMANTIC_VIRTUAL_STREAM_EXCHANGE, routing_key=SEMANTIC_VIRTUAL_STREAM_ROUTING_KEY,
                          body=json.dumps({ID: stream_id, METADATA: semantic_virtual_stream}))
    connection.close()


def subscribe_to_scream_update():
    connect = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connect.channel()

    channel.exchange_declare(exchange=STREAM_EXCHANGE, type=EXCHANGE_TYPE)

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=STREAM_EXCHANGE, queue=queue_name, routing_key=STREAM_ROUTING_KEY)

    channel.basic_consume(__callback_stream, queue=queue_name, no_ack=True)
    channel.start_consuming()


def subscribe_to_virtual_scream_update():
    connect = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connect.channel()

    channel.exchange_declare(exchange=VIRTUAL_STREAM_EXCHANGE, type=EXCHANGE_TYPE)

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=VIRTUAL_STREAM_EXCHANGE, queue=queue_name, routing_key=VIRTUAL_STREAM_ROUTING_KEY)

    channel.basic_consume(__callback_virtual_stream, queue=queue_name, no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    logging.basicConfig()
    subscribe_to_scream_update()
    subscribe_to_virtual_scream_update()
