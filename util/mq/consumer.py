# coding=utf-8

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


def consume_mq(q):
    credentials = pika.PlainCredentials('miya_amqp_admin', 'miya_admin_pwd')
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.96.87', 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(q, True)
    channel.basic_consume(q, callback, True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# consume_mq("partner.promotion.monitored.queue")
consume_mq("groupon.order.left.pay.success.queue")
