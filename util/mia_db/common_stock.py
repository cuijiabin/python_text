# coding=utf-8
import json

import requests

import util as bm
import util.mia_db as mu
from threading import Timer
from rediscluster import RedisCluster


# 库存redis集群
def get_cluster_client():
    redis_nodes = [
        {'host': '10.5.96.169', 'port': 7012},
        {'host': '10.5.96.174', 'port': 7012},
        {'host': '10.5.96.181', 'port': 7012},
        {'host': '10.5.96.228', 'port': 7024},
        {'host': '10.5.97.18', 'port': 7024},
        {'host': '10.5.96.169', 'port': 7013}
    ]

    return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)


def gen_stock_key(item_id):
    return "stock_" + str(item_id)


def gen_change_key(item_id):
    return "stock_" + str(item_id) + "_incr"


def gen_pre_qty_lock_key(item_id, wid):
    return "stock_init_pre_qty_lock_" + str(item_id) + "_" + str(wid)


def gen_stock_test_key(item_id):
    return "stock_" + str(item_id) + "_test"


def gen_change_test_key(item_id):
    return "stock_" + str(item_id) + "_test_incr"


# 获取预占的filed
def gen_pre_qty_field(wid):
    return "wid_" + str(wid) + "_preQty"


# 获取库存数量的filed
def gen_qty_field(wid):
    return "wid_" + str(wid) + "_qty"


# 根据itemId 获取redis库存
def get_stock(item_id):
    redis_client = get_cluster_client()
    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


# 根据itemId 获取redis测试库存
def get_test_stock(item_id):
    redis_client = get_cluster_client()

    stock_key = gen_stock_test_key(item_id)
    change_key = gen_change_test_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


# 根据itemId 删除redis库存
def delete_stock(item_id):
    redis_client = get_cluster_client()

    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))

    redis_client.delete(stock_key)
    redis_client.delete(change_key)


# 增加预占库存
def add_pre_qty_stock(item_id, wid):
    redis_client = get_cluster_client()

    stock_key = gen_stock_key(item_id)
    pre_qty_field = gen_pre_qty_field(wid)

    redis_client.hincrby(stock_key, pre_qty_field, 1)

    change_key = gen_change_key(item_id)
    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


'''
select * from stock_item WHERE item_id = 5021462;

select  count(oi.id) as number from order_item oi ,orders os
        where oi.order_id =os.id
        and os.warehouse_id= (select warehouse_id from stock_item WHERE item_id = 5021462)
        and os.status in(1,2)
        and os.wdgj_status=1
        and os.is_test=0
        and oi.stock_item_id= (select id from stock_item WHERE item_id = 5021462)
        group by oi.stock_item_id;
'''


def batch_delete_pre_init():
    init_keys = ['3070146_6789']

    redis_client = get_cluster_client()
    for key in init_keys:
        lock_key = "stock_init_pre_qty_lock_" + key
        print(redis_client.get(lock_key))
        redis_client.delete(lock_key)


def test_tup():
    stock_list = [(1, 2), (4, 7)]
    for stock in stock_list:
        print(gen_pre_qty_lock_key(stock[0], stock[1]))


# 根据仓库id获取可用库存列表
def get_stock_item(wid):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT * FROM stock_item WHERE warehouse_id = " + str(wid) + " AND status = 1 ORDER BY modify_time DESC"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


# 根据仓库id检查预占库存
def check_pre_qty(wid):
    stock_list = get_stock_item(wid)
    if len(stock_list) < 1:
        print("可用库存列表为空 wid = ", wid)
        return

    redis_client = get_cluster_client()
    for stock in stock_list:
        item_id = stock['item_id']
        stock_key = gen_stock_key(item_id)
        pre_qty_field = gen_pre_qty_field(wid)
        redis_pre_qty = redis_client.hget(stock_key, pre_qty_field)
        if redis_pre_qty is None:
            # print("预占库存不存在 stock_item_id = %d, item_id = %d, wid = %d " % (stock['id'], item_id, wid))
            continue

        amount = stock['pre_qty'] - int(redis_pre_qty)
        if amount != 0:
            print(
                "预占库存有差异 stock_item_id = %d, item_id = %d, wid = %d, amount= %d " % (stock['id'], item_id, wid, amount))


# 根据仓库id批量检查预占库存
def batch_check_pre_qty(wid_list=[]):
    if len(wid_list) == 0:
        wid_list = [6789]
    for wid in wid_list:
        check_pre_qty(wid)


'''
1.db 预占与 订单不一致 需要清理 init 库存
2.db 与 订单一致 但是与redis不一致 则只清理库存即可！
'''


# 通过接口获取库存列表详情
def get_all_stock_list(item_id_list=[3070022]):
    param_list = []
    for item_id in item_id_list:
        param_list.append({"itemId": item_id, "warehouseIds": [], "isExact": 0})

    r_data = {"paramJSON": json.dumps(param_list)}
    r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)

    content = json.loads(r.content.decode("utf-8"))
    print(content["result"])


def check_all_by_stock_item_id(stock_item_id=5291074, is_modify=False):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT * FROM stock_item WHERE id = " + str(stock_item_id)
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    db_item = dict(zip(columns, cur.fetchall()[0]))

    item_id = db_item["item_id"]
    wid = db_item["warehouse_id"]

    order_sql = "select ifnull(count(oi.id), 0) as number " \
                "from order_item oi left join orders os on oi.order_id = os.id " + \
                "where os.warehouse_id= " + str(wid) + \
                " and os.status in(1,2) and os.wdgj_status=1 and os.is_test= 0 " + \
                "and oi.stock_item_id= " + str(db_item["id"]) + \
                " group by oi.stock_item_id"
    cur.execute(order_sql)
    fetch = cur.fetchall()
    order_count = (0 if (len(fetch) == 0) else fetch[0][0])

    redis_client = get_cluster_client()
    stock_key = gen_stock_key(item_id)
    pre_qty_field = gen_pre_qty_field(wid)
    redis_pre_qty = redis_client.hget(stock_key, pre_qty_field)
    redis_pre_qty = int(redis_pre_qty)

    if order_count != db_item["pre_qty"]:
        print("预占库存与订单不一致 stock_item_id = %d, db_pre_qty = %d, order_count= %d"
              % (stock_item_id, db_item["pre_qty"], order_count))
        if is_modify:
            pre_qty_lock_key = gen_pre_qty_lock_key(item_id, wid)
            redis_client.delete(pre_qty_lock_key)
            redis_client.delete(stock_key)
            # 刷新
            param_list = [{"itemId": item_id, "warehouseIds": [wid], "isExact": 0}]
            r_data = {"paramJSON": json.dumps(param_list)}
            r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
            content = json.loads(r.content.decode("utf-8"))
            print(content["result"])

    elif redis_pre_qty != db_item["pre_qty"]:
        print("预占库存与redis不一致 stock_item_id = %d, db_pre_qty = %d, redis_pre_qty= %d"
              % (stock_item_id, db_item["pre_qty"], redis_pre_qty))
        if is_modify:
            redis_client.delete(stock_key)
            # 刷新
            param_list = [{"itemId": item_id, "warehouseIds": [wid], "isExact": 0}]
            r_data = {"paramJSON": json.dumps(param_list)}
            r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
            content = json.loads(r.content.decode("utf-8"))
            print(content["result"])


if __name__ == "__main__":
    wid_list = [70, 73, 90, 101, 133, 139, 151, 193, 203, 295, 331, 332, 337, 373, 385, 389, 401, 406, 438, 471, 552,
                553, 614, 654, 674, 708, 716, 817, 883, 896, 1007, 1114, 1149, 1258, 1266, 1280, 1308, 1309, 1349,
                1384, 1484, 1492, 1511, 1621, 1632, 1637, 1640, 1669, 1701, 1730, 1744, 1758, 1870, 1969, 1972, 2091,
                2133, 2143, 2153, 2233, 2430, 2460, 2479, 2622, 2655, 2681, 2701, 2710, 2719, 2724, 2792, 2801, 2802,
                2841, 2842, 2844, 2896, 2923, 2938, 2964, 2990, 3025, 3033, 3036, 3043, 3045, 3046, 3057, 3070, 3071,
                3098, 3114, 3118, 3122, 3130, 3225, 3248, 3296, 3391, 3410, 3424, 3452, 3507, 3610, 3658, 3716, 3737,
                3806, 3934, 4069, 4247, 4270, 4277, 4281, 4283, 4355, 4521, 4528, 4715, 4743, 4831, 4838, 4854, 4859,
                4860, 4866, 5188, 5197, 5249, 5342, 5569, 5620, 5641, 5645, 5717, 5786, 5879, 5919, 5923, 5944, 6053,
                6139, 6380, 6400, 6412, 6434, 6438, 6514, 6537, 6549, 6582, 6603, 6604, 6617, 6629, 6630, 6640, 6675,
                6678, 6700, 6735, 6750, 6773, 6794, 6800, 6806, 6874, 6875, 6876, 6879, 6885, 6888, 6891, 6894, 6902,
                6903, 6906, 6910, 6918, 6921, 6927, 6953, 6955, 6956, 6957, 6962, 6964, 6965, 6970, 6982, 6983, 6989,
                6996, 7002, 7004, 7008, 7018, 7022, 7040, 7041, 7042, 7046, 7047, 7052, 7054, 7056, 7061, 7063, 7066,
                7071, 7078, 7084, 7087, 7100, 7102, 7106, 7108, 7109, 7110, 7113, 7117, 7118, 7126, 7127, 7129, 7131,
                7133, 7135, 7137, 7151, 7156, 7158, 7161, 7162, 7164, 7166, 7167, 7168, 7171, 7178, 7190, 7201, 7205,
                7208, 7213, 7214, 7215, 7216, 7218, 7222, 7226, 7230, 7241, 7250, 7255, 7265, 7273, 7279, 7284, 7285,
                7294, 7300, 7301, 7305, 7313, 7322, 7325, 7329, 7335, 7336, 7351, 7353, 7355, 7358, 7362, 7364, 7367,
                7371, 7378, 7388, 7389, 7392, 7394, 7399, 7400, 7401, 7402, 7406, 7408, 7421, 7423, 7427, 7431, 7437,
                7441, 7443, 7454, 7472, 7474, 7477, 7486, 7487, 7488, 7489, 7494, 7501, 7506, 7507, 7520, 7578, 7585,
                7588, 7589, 7592, 7599, 7609, 7610, 7614, 7616, 7622, 7626, 7636, 7648, 7649, 7656, 7662, 7663, 7664,
                7672, 7679, 7680, 7690, 7692, 7696, 7699, 7703, 7705, 7706, 7711, 7712, 7713, 7715, 7717, 7719, 7721,
                7733, 7734, 7735, 7737, 7739, 7749, 7751, 7755, 7757, 7760, 7765, 7775, 7784, 7793, 7797, 7802, 7804,
                7806, 7807, 7810, 7811, 7815, 7819, 7820, 7821, 7825, 7830, 7831, 7839, 7842, 7849, 7851, 7854, 7859,
                7861, 7862, 7864, 7866, 7869, 7872, 7873, 7877, 7890, 7891, 7896, 7897, 7899, 7912, 7914, 7917, 7918,
                7921, 7922, 7923, 7925, 7927, 7928, 7929, 7930, 7931, 7932, 7933, 7934, 7936, 7937, 7938, 7940, 7943,
                7945, 7946, 7951, 7956, 7958, 7961, 7966, 7969, 7971, 7972, 7974]
    # get_all_stock_list(item_list)
    # get_stock(3070022)
    # check_all_by_stock_item_id(7474882, True)
    batch_check_pre_qty(wid_list)
