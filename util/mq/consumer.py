# coding=utf-8

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


def consume_mq(q):
    credentials = pika.PlainCredentials('root', 'root')
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.104.185', 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(q, True)
    channel.basic_consume(q, callback, True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# consume_mq("partner.promotion.monitored.queue")
consume_mq("order.pay.sync.queue")
