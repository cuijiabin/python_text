# coding=utf-8
import redis


# 查看redis版本信息
def get_redis_info():
    r = redis.StrictRedis(host='172.16.104.185', port=6379, db=0)
    print(r.info())


if __name__ == '__main__':
    get_redis_info()
