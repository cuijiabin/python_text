# coding=utf-8


import pika


def send_mq(publish_map, body_content):
    credentials = pika.PlainCredentials('miya_amqp_admin', 'miya_admin_pwd')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.5.1.25', 5672, '/', credentials))
    # credentials = pika.PlainCredentials('test', '123456')
    # connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.130.142', 5672, '/', credentials))
    channel = connection.channel()

    # 声明queue
    channel.queue_declare(publish_map["queue"], True)
    headers = {"__TypeId__": "java.lang.String"}
    properties = pika.BasicProperties('application/json', 'UTF-8', headers, 1, 0)
    channel.basic_publish(publish_map["exchange"], publish_map["routing_key"], body_content, properties)
    print(" [x] Sent %r" % body_content)
    connection.close()


def send_headers_mq(headers, publish_map, body_content):
    credentials = pika.PlainCredentials('miya_amqp_admin', 'miya_admin_pwd')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.5.1.25', 5672, '/', credentials))
    channel = connection.channel()

    # 声明queue
    channel.queue_declare(publish_map["queue"], True)
    headers = {"__TypeId__": headers}
    properties = pika.BasicProperties('application/json', 'UTF-8', headers, 1, 0)
    channel.basic_publish(publish_map["exchange"], publish_map["routing_key"], body_content, properties)
    print(" [x] Sent %r" % body_content)
    connection.close()


if __name__ == "__main__":
    # paramsMap = {
    #     "subOrderId": "700002976",
    #     "orderCode": "1909257000029765",
    #     "parentDstSheetId": 2254,
    #     "userId": 220107054
    # }
    #
    # audit_publish_map = {
    #     "queue": "partner.item.audit.check.queue_dev",
    #     "exchange": "partner.item.audit.check.exchange",
    #     "routing_key": "partner.item.audit.check.routkey"
    # }
    #
    # insurance_send_map = {
    #     "queue": "partner.order.send.delay.queue",
    #     "exchange": "partner.order.send.delay.exchange",
    #     "routing_key": "partner.order.send.delay.routkey"
    # }
    #
    # group_send_map = {
    #     "queue": "groupon.order.left.pay.success.queue",
    #     "exchange": "groupon.order.left.pay.success.exchange",
    #     "routing_key": "groupon.order.left.pay.success.routkey"
    # }
    #
    # group_pay_map = {
    #     "queue": "groupon.order.pay.success.queue",
    #     "exchange": "groupon.order.pay.success.exchange",
    #     "routing_key": "groupon.order.pay.success.routkey"
    # }
    #
    # front_pay_map = {
    #     "queue": "order.pay.sync.queue",
    #     "exchange": "order.pay.sync.exchange",
    #     "routing_key": "order.pay.sync.routeKey"
    # }
    pd_group_pay_map = {
        "queue": "local_groupon.order.pay.success.queue",
        "exchange": "local_groupon.order.pay.success.exchange",
        "routing_key": "local_groupon.order.pay.success.routkey"
    }

    order_filter_map = {
        "queue": "order.filter.queue",
        "exchange": "order.filter.exchange",
        "routing_key": "order.filter.routkey"
    }

    # 订单风控处理
    send_mq(order_filter_map, "202110122456386180")

    # send_mq(insurance_send_map, '"{\\"subOrderId\\":\\"700003185\\",\\"orderCode\\":\\"1909297000031853\\",'
    #                             '\\"parentDstSheetId\\":2312,\\"userId\\":220105928}"')

    # send_mq(group_send_map, '"{\\"superiorOrderCode\\":\\"202002197000056064\\",\\"fromType\\":4,,\\"status\\":1,'
    #                         '\\"relationId\\":16936121,\\"userId\\":220109011}"')
    # send_headers_mq("com.mia.srv.orderpd.mq.GrouponOrderInfo", pd_group_pay_map,
    #                 '{"superiorOrderCode":"202108262448474312","status":1,"fromType":18,"relationId":36313,"userId":46328566}')
