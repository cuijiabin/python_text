# coding=utf-8
import util as bm


# 线上master
def get_set_info():
    r = bm.get_single_redis_client()
    # print(r.exists("crm_strategy_task_zset"))
    # s = r.zscan("crm_strategy_task_zset", 20)
    # print(s)
    # print(r.hgetall("crm_group_910_b_2020-12-28"))
    mm = r.hgetall("crm_group_910_a_2020-12-28")
    for m in mm:
        print(str(m))
    # print(r.hset("crm_1_a_2020-03-27", "43784202", "0"))


if __name__ == '__main__':
    r = bm.get_single_redis_client()

    ll = [202111162465233593]

    for s in ll:
        print(str(s), r.get("order_add_gift_tmp_" + str(s)))
