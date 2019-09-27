# coding=utf-8


import pika


def send_mq(publish_map, body_content):
    credentials = pika.PlainCredentials('miya_amqp_admin', 'miya_admin_pwd')
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.96.87', 5672, '/', credentials))
    channel = connection.channel()

    # 声明queue
    channel.queue_declare(publish_map["queue"], True)
    headers = {"__TypeId__": "java.lang.String"}
    properties = pika.BasicProperties('application/json', 'UTF-8', headers, 1, 0)
    channel.basic_publish(publish_map["exchange"], publish_map["routing_key"], body_content, properties)
    print(" [x] Sent %r" % body_content)
    connection.close()


if __name__ == "__main__":
    paramsMap = {
        "subOrderId": "700002976",
        "orderCode": "1909257000029765",
        "parentDstSheetId": 2254,
        "userId": 220107054
    }

    audit_publish_map = {
        "queue": "partner.item.audit.check.queue_dev",
        "exchange": "partner.item.audit.check.exchange",
        "routing_key": "partner.item.audit.check.routkey"
    }

    insurance_send_map = {
        "queue": "partner.order.send.delay.queue",
        "exchange": "partner.order.send.delay.exchange",
        "routing_key": "partner.order.send.delay.routkey"
    }

    # send_mq(insurance_send_map, json.dumps(paramsMap))

    send_mq(insurance_send_map, '"{\\"subOrderId\\":\\"700002976\\",\\"orderCode\\":\\"1909257000029765\\",'
                                '\\"parentDstSheetId\\":2254,\\"userId\\":220107054}"')
    # send_mq(insurance_send_map,'"{\\"supplierId\\":12386,\\"type\\":1}"')
