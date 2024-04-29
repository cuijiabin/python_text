# coding=utf-8

import random
import time
import paho.mqtt.client as mqtt


# 创建mqtt链接
def create_mqtt_clients(topic_list):
    def on_connect(rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client_list = []
    for inner_topic in topic_list:
        client_id = f'python-mqtt-{random.randint(0, 100)}'
        client = mqtt.Client(client_id)
        client.username_pw_set("admin", password="cctd@2015")
        client.on_connect = on_connect
        client.connect("192.168.4.38", 1883)
        client_list.append({"client": client, "topic": inner_topic})
    return client_list


# 发送消息
def publish_message(client, topic, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


# 发布消息的模板
message_base = ["$v1", "1706077352389", "DQ/GF/YQ/SD_001838",
                "66.7",  # 1	风机实时发电量
                "817.4",  # 2	上网电量
                "818.5",  # 3	日总发电量
                "816.6",  # 4	月总发电量
                "1415.77",  # 5	年总发电量
                "0.59",  # 6	弃风率
                "1414.39",  # 7	功率预测情况
                "520.0",  # 8	装机容量
                "1814.39",  # 9	实时功率
                "0.92",  # 10	出力率
                "30",  # 11	风机总数
                "18",  # 12	运行数量
                "12",  # 13	停机数量
                "1200.10",  # 14	有功功率
                "300.43",  # 15	无功功率
                "0.57",  # 16	功率因数
                "20.16",  # 17	扭缆角度
                "3.276",  # 18	机舱角度
                "0.9",  # 19	设备月利用率
                "9296.21",  # 20	日运行小时
                "11381.1",  # 21	齿轮箱压力
                "18.08",  # 22	液压站压力
                "30.0",  # 23	变频器温度
                "8.68",  # 24	叶片1角度
                "10.11",  # 25	叶片2角度
                "30.0",  # 26	叶片3角度
                "66.0",  # 27	1号变桨电机温度
                "67.6",  # 28	2号变桨电机温度
                "70.0",  # 29	3号变桨电机温度
                "5.4",  # 30	齿轮箱振动值1
                "6.4",  # 31	齿轮箱振动值2
                "0.82",  # 32	日可利用率
                "10.59",  # 33	平均风速
                "3.0",  # 34	风向
                "1.0",  # 35	状态
                "#"]


# 获取开关数据 0或1
def get_switch_num():
    return round(random.choice([0.0, 1.0]), 1)


# 根据范围与精度获取浮点数
def get_data_with_precision(start, end, precision):
    random_float = round(random.uniform(start, end), precision)
    return random_float


def run():
    # 生成topic列表
    topics = [f"DQ/GF/FYQ/SD_0000{str(i).zfill(2)}" for i in range(1, 11)]
    mqtt_clients = create_mqtt_clients(topics)

    while True:
        time_stamp = str(round(time.time() * 1000))
        print(time_stamp)
        # 打印每个客户端的topic
        for client_info in mqtt_clients:
            print(f"Client: {client_info['client']}, Topic: {client_info['topic']}")
            topic = client_info["topic"]
            message = message_base.copy()
            message[1] = time_stamp
            message[2] = topic
            message[37] = str(round(random.choice([0.0, 1.0]), 1))

            message[3] = str(get_data_with_precision(60, 90, 2))
            message[4] = str(get_data_with_precision(800, 1200, 2))
            message[5] = str(get_data_with_precision(800, 1200, 2))
            message[6] = str(get_data_with_precision(24000, 36000, 2))
            message[7] = str(get_data_with_precision(240000, 360000, 2))

            message[8] = str(get_data_with_precision(0, 100, 2))
            message[9] = str(get_data_with_precision(900, 1800, 2))
            message[10] = str(get_data_with_precision(520, 520, 2))
            message[11] = str(get_data_with_precision(1800, 2000, 2))
            message[12] = str(get_data_with_precision(0, 100, 2))

            # 风机数量模拟
            rum_num = get_data_with_precision(18, 30, 0)
            stop_num = 30 - rum_num
            message[13] = str(30)
            message[14] = str(rum_num)
            message[15] = str(stop_num)

            message[16] = str(get_data_with_precision(1400, 1800, 2))
            message[17] = str(get_data_with_precision(400, 600, 2))
            message[18] = str(get_data_with_precision(0, 1, 2))
            message[19] = str(get_data_with_precision(0, 360, 2))
            message[20] = str(get_data_with_precision(0, 360, 2))
            message[21] = str(get_data_with_precision(0, 100, 2))
            message[22] = str(get_data_with_precision(0, 18, 2))
            message[23] = str(get_data_with_precision(600, 700, 2))
            message[24] = str(get_data_with_precision(600, 700, 2))
            message[25] = str(get_data_with_precision(7, 70, 2))
            message[26] = str(get_data_with_precision(0, 360, 2))
            message[27] = str(get_data_with_precision(0, 360, 2))
            message[28] = str(get_data_with_precision(0, 360, 2))
            message[29] = str(get_data_with_precision(7, 70, 2))
            message[30] = str(get_data_with_precision(7, 70, 2))
            message[31] = str(get_data_with_precision(7, 70, 2))
            message[32] = str(get_data_with_precision(10, 50, 2))
            message[33] = str(get_data_with_precision(10, 50, 2))
            message[34] = str(get_data_with_precision(80, 100, 2))
            message[35] = str(get_data_with_precision(5, 30, 2))
            message[36] = str(get_data_with_precision(0, 360, 2))

            publish_message(client_info["client"], topic, ",".join(message))
        time.sleep(10)


if __name__ == '__main__':
    run()
