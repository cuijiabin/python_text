import time

import requests
from rediscluster import RedisCluster

import redis

db = redis.Redis(host='10.5.111.131', port=6379, decode_responses=True)
print("总共涉及用户数量", db.get("user_job:tmp_sum_2019_user_update"))
print("更新的mibean累积减少量", db.get("user_job:tmp_sum_2019_mibean_reduce"))
print("更新的mibean累积增加量", db.get("user_job:tmp_sum_2019_mibean_increase"))
print("总共过期涉及的用户数量", db.get("user_job:tmp_sum_2019_user_expire"))
print("过期的蜜豆总数", db.get("user_job:tmp_sum_2019_mibean_expire"))

#
# # 库存redis集群
# def get_cluster_client():
#     redis_nodes = [
#         {'host': '10.5.111.131', 'port': 6379},
#         {'host': '10.5.111.6', 'port': 6379}
#     ]
#
#     return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)
#
#
# def run_export_data():
#     redis_client = get_cluster_client()
#     print(redis_client.get("user_job:tmp_sum_2019_user_update"))
#
#
# if __name__ == '__main__':
#     run_export_data()
