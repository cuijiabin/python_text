# coding=utf-8
import redis


# 查看redis版本信息
# def get_redis_info():
#     r = redis.StrictRedis(host='172.16.104.185', port=6379, db=0)
#     print(r.info())

# 线上master
def get_set_info():
    r = redis.StrictRedis(host='10.5.111.125', port=6379, db=0)
    # print(r.exists("crm_strategy_task_zset"))
    # s = r.zscan("crm_strategy_task_zset", 20)
    # print(s)
    # print(r.hgetall("crm_group_910_b_2020-12-28"))
    mm = r.hgetall("crm_group_910_a_2020-12-28")
    for m in mm:
        print(str(m))
    # print(r.hset("crm_1_a_2020-03-27", "43784202", "0"))


if __name__ == '__main__':
    r = redis.StrictRedis(host='10.5.111.125', port=6379, db=0)

    m_list = ['15225860225']
    wx_list = ['oRMfI5Y2zmdJHP_iAugHTAGXsZm8']
    for m in wx_list:
        print(m, r.hget("yao_xin_groupon_v3_dst_mobile_115", m))
        # print(m, r.hdel("yao_xin_groupon_v3_dst_mobile_115", m))
    for m in m_list:
        print(m, r.hget("yao_xin_groupon_v3_open_id_115", m))
        # print(m, r.hdel("yao_xin_groupon_v3_open_id_115", m))
