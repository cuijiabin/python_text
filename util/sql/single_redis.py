# coding=utf-8
import redis


# 查看redis版本信息
def get_redis_info():
    r = redis.StrictRedis(host='172.16.104.185', port=6379, db=0)
    print(r.info())


def get_set_info():
    r = redis.StrictRedis(host='172.16.104.185', port=6379, db=0)
    # print(r.exists("crm_strategy_task_zset"))
    # s = r.zscan("crm_strategy_task_zset", 20)
    # print(s)
    print(r.hgetall("crm_1_a_2020-03-27"))
    # print(r.hset("crm_1_a_2020-03-27", "43784202", "0"))


if __name__ == '__main__':
    get_set_info()
