from lib import broker

__author__ = 'ehonlia'

import pika
import logging

logging.basicConfig()

connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker.HOST))
channel = connection.channel()

channel.exchange_declare(exchange=broker.STREAM_EXCHANGE, type=broker.EXCHANGE_TYPE)

message = '''
{
  "_index": "sensorcloud",
  "_source": {
    "polling": false,
    "min_val": "0",
    "nr_subscribers": 0,
    "uri": "",
    "name": "[ER Day 2013] Battery North",
    "resource": {
      "resource_type": "",
      "uuid": ""
    },
    "active": true,
    "subscribers": [],
    "user_ranking": {
      "average": 60,
      "nr_rankings": 1
    },
    "unit": "",
    "quality": 1,
    "history_size": 6995,
    "polling_freq": 0,
    "creation_date": "2014-01-09",
    "private": false,
    "parser": "",
    "last_updated": "2014-01-21T16:26:50.000",
    "user_id": "user",
    "location": {
      "lon": 17.949467700000014,
      "lat": 59.40325599999999
    },
    "type": "battery level",
    "accuracy": "",
    "description": "battery level of the mote on the North pipe (not leaky)",
    "data_type": "application/json",
    "tags": "battery charge",
    "max_val": "255"
  },
  "_id": "abcdef",
  "_type": "stream",
  "_score": 1
}
'''
channel.basic_publish(exchange=broker.STREAM_EXCHANGE,
                      routing_key=broker.STREAM_ROUTING_KEY,
                      body=message)
print " [x] Sent %r:%r" % (broker.STREAM_ROUTING_KEY, message)
connection.close()
