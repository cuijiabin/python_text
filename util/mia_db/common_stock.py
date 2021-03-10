# coding=utf-8
import json
import time
from itertools import islice

import requests
from vthread import vthread

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
    # change_key = gen_change_key(item_id)
    # qty_key = gen_qty_field(7575)

    # print(item_id, redis_client.hget(stock_key, qty_key))
    print(item_id, redis_client.hgetall(stock_key))


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
    sql = "SELECT id,item_id,pre_qty FROM stock_item WHERE warehouse_id = " + str(
        wid) + " AND status = 1 AND modify_time > ADDDATE(NOW(),INTERVAL -1 HOUR) ORDER BY modify_time DESC"
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
            print("预占库存不存在 stock_item_id = %d, item_id = %d, wid = %d " % (stock['id'], item_id, wid))
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
    fetch = cur.fetchall()
    if len(fetch) == 0:
        print("数据库查询失败", stock_item_id)
        return
    db_item = dict(zip(columns, fetch[0]))

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
    if redis_pre_qty is None:
        print("预占库存不存在 stock_item_id = %d" % stock_item_id)
        return

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


# 批量检查库存
def batch_check_all_by_stock_item_id(stock_id_list=[6985391], is_modify=False):
    cur = bm.get_mia_cursor("mia_mirror")
    for stock_item_id in stock_id_list:

        sql = "SELECT * FROM stock_item WHERE id = " + str(stock_item_id)
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        fetch = cur.fetchall()
        if len(fetch) == 0:
            print("数据库查询失败", stock_item_id)
            return
        db_item = dict(zip(columns, fetch[0]))

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
        if redis_pre_qty is None:
            print("预占库存不存在 stock_item_id = %d" % stock_item_id)
            return

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
    cur.close()


# @vthread.pool(1)
def l_read_file(filename, N):
    with open(filename, 'r') as infile:
        lines_gen = islice(infile, N)
        ids = list(map(lambda x: x.strip('\n'), lines_gen))
        while len(ids) > 0:
            stock_item_ids = ",".join(ids)
            r_data = {
                "stockItemIds": stock_item_ids,
                "type": 1
            }
            r = requests.post("http://10.5.107.234:7777/repairPreQty.sc", data=r_data)
            content = json.loads(r.content.decode("utf-8"))
            if len(content) > 0:
                for c in content:
                    if c["content"] == "预占库存与订单不一致" or c["content"] == "预占库存与redis不一致":
                        # if c["content"] == "预占库存与redis不一致":
                        print(c)

            time.sleep(0.5)
            lines_gen = islice(infile, N)
            ids = list(map(lambda x: x.strip('\n'), lines_gen))
    infile.close()


def re_send_mq(mq):
    r = requests.post("http://127.0.0.1:9089/stock/reSendMq", data=mq)

    print(r.content.decode("utf-8"))


''''' 
   每n秒执行一次 
'''


def timer_task(n):
    while True:
        print(time.strftime('%Y-%m-%d %X', time.localtime()))
        l_read_file("E:/file/download/tt/filter.txt", 500)
        time.sleep(n * 60)


def check_warehouse_qty(wid_list=[7694, 7697]):
    while True:
        print(time.strftime('%Y-%m-%d %X', time.localtime()))
        ids = []
        for wid in wid_list:
            rows = get_stock_item(wid)
            tmp_ids = list(map(lambda x: x['id'], rows))
            for stock_id in tmp_ids:
                ids.append(str(stock_id))

        print(len(ids))
        if len(ids) > 0:
            stock_item_ids = ",".join(ids)
            r_data = {
                "stockItemIds": stock_item_ids,
                "type": 1
            }
            r = requests.post("http://10.5.107.234:7777/repairPreQty.sc", data=r_data)
            content = json.loads(r.content.decode("utf-8"))
            if len(content) > 0:
                for c in content:
                    if c["content"] == "预占库存与订单不一致" or c["content"] == "预占库存与redis不一致":
                        print(c)
        time.sleep(10 * 60)


def re_send_mq(mq):
    r = requests.post("http://10.5.105.104:9089/stock/reSendMq", data=mq)

    print(r.content.decode("utf-8"))


# -- 库存同步比较
# select b.item_id, b.warehouse_id, b.id, s.item_id
# from mia_bmp.brand_stock_item_channel b
# left join mia_mirror.stock_item s on b.item_id=s.item_id and b.warehouse_id=s.warehouse_id and b.channel_id=1
# where b.channel_id=1 AND s.item_id is NULL;
def clear_bmp_pre_qty():
    t_list = [(4210722, 8117), (4210723, 8117), (2860759, 8117), (5070593, 8117), (5596530, 8117), (5070594, 8117),
              (5546642, 8117), (5502654, 8117), (5132928, 8117), (5132926, 8117), (4752037, 8117), (5546641, 8117),
              (5502662, 8117), (4484371, 8117), (5255618, 8117), (5506461, 8117), (5206946, 8117), (5116773, 8117),
              (5502651, 8117), (5506457, 8117), (5502649, 8117), (5116768, 8117), (5293710, 8117), (5506456, 8117),
              (5506460, 8117), (4284949, 8117), (5486206, 8117), (4484372, 8117), (5546637, 8117), (5376976, 8117),
              (5481589, 8117), (5096237, 8117), (5092974, 8117), (4548492, 8117), (2481497, 8117), (1817607, 8117),
              (5486228, 8117), (5486215, 8117), (5514010, 8117), (5481593, 8117), (5092972, 8117), (5546629, 8117),
              (4422071, 8117), (5460750, 8117), (2426338, 8117), (3035633, 8117), (5481601, 8117), (4484374, 8117),
              (4422070, 8117), (2495703, 8117), (5559301, 8117), (4948639, 8117), (5315749, 8117), (5481585, 8117),
              (5009097, 8117), (2802734, 8117), (5461009, 8117), (5481576, 8117), (2802540, 8117), (5486196, 8117),
              (5489628, 8117), (5486204, 8117), (5481600, 8117), (5559546, 8117), (5096236, 8117), (5502664, 8117),
              (5092976, 8117), (3039863, 8117), (2506746, 8117), (2474573, 8117), (5261758, 8117), (4774851, 8117),
              (5096240, 8117), (5486218, 8117), (2961469, 8117), (5132927, 8117), (5116771, 8117), (5009094, 8117),
              (5481578, 8117), (5460751, 8117), (5481574, 8117), (5460767, 8117), (5460765, 8117), (5460760, 8117),
              (5460762, 8117), (5460766, 8117), (5460764, 8117), (5352455, 8117), (5489627, 8117), (5489615, 8117),
              (5521173, 8117), (5318580, 8117), (5096235, 8117), (2793988, 8117), (5486201, 8117), (5481570, 8117),
              (5546640, 8117), (3035634, 8117), (4463219, 8117), (4644507, 8117), (5116770, 8117), (4948640, 8117),
              (2802732, 8117), (4644500, 8117), (3039866, 8117), (5546643, 8117), (5546639, 8117), (5481572, 8117),
              (5460756, 8117), (5502647, 8117), (5546630, 8117), (5521181, 8117), (5460749, 8117), (5460761, 8117),
              (5489624, 8117), (5413267, 8117), (5521174, 8117), (5546636, 8117), (5481594, 8117), (5410062, 8117),
              (5502665, 8117), (5481571, 8117), (2734559, 8117), (5096239, 8117), (5092970, 8117), (2481492, 8117),
              (5092968, 8117), (3035631, 8117), (5489626, 8117), (5116774, 8117), (5009096, 8117), (5009095, 8117),
              (5481596, 8117), (5301775, 8117), (5489617, 8117), (5481595, 8117), (5357346, 8117), (5132924, 8117),
              (5481587, 8117), (5481590, 8117), (5460758, 8117), (5410064, 8117), (4644504, 8117), (3035630, 8117),
              (5486234, 8117), (2623072, 8117), (1817605, 8117), (5096241, 8117), (5486216, 8117), (5489616, 8117),
              (5489625, 8117), (4484375, 8117), (4463683, 8117), (4484373, 8117), (5546628, 8117), (5474711, 8117),
              (5481597, 8117), (5481575, 8117), (5565213, 8117), (5546638, 8117), (5474712, 8117), (5546631, 8117),
              (5486200, 8117), (5502655, 8117), (5092969, 8117), (3807605, 8117), (2474565, 8117), (2474342, 8117),
              (5261757, 8117), (2436952, 8117), (5460752, 8117), (3035632, 8117), (5502648, 8117), (5376323, 8117),
              (5132925, 8117), (4948636, 8117), (5482954, 8117), (5481599, 8117), (5116769, 8117), (4948638, 8117),
              (5521182, 8117), (5613405, 8117), (5481577, 8117), (4992192, 8117), (5546632, 8117), (3039864, 8117),
              (5461011, 8117), (5460763, 8117), (5460768, 8117), (5460759, 8117), (5481569, 8117), (5585123, 8117),
              (4644501, 8117), (5502663, 8117), (5546635, 8117), (2562692, 8117), (5481591, 8117), (5486198, 8117),
              (5486199, 8117), (5096238, 8117), (5092971, 8117), (5486217, 8117), (1817606, 8117), (5486197, 8117),
              (5474710, 8117), (2474174, 8117), (5460757, 8117), (4310649, 8117), (4992193, 8117), (5292750, 8117),
              (5481573, 8117), (5481586, 8117), (4968389, 8117), (5486227, 8117), (5481588, 8117), (5474714, 8117),
              (5486205, 8117), (5481598, 8117), (5489629, 8117), (5092975, 8117), (5096234, 8117), (5377045, 8117),
              (5502650, 8117), (3039865, 8117), (5460753, 8117), (5565214, 8117), (5376324, 8117), (5546633, 8117),
              (2802733, 8117), (4644502, 8117), (4644503, 8117), (5481592, 8117), (5474713, 8117), (5461010, 8117),
              (2474252, 8117), (4774852, 8117), (2474190, 8117), (4775081, 8117), (2474245, 8117), (4775509, 8117),
              (2474253, 8117), (2506747, 8117), (2474219, 8117), (4774850, 8117), (4948633, 8117), (4948631, 8117),
              (4948632, 8117), (5461013, 8117), (5461012, 8117), (5461014, 8117), (5546644, 8117), (2991889, 3364),
              (2991888, 3364), (2912505, 3364), (1690845, 3364), (1690849, 3364), (5673983, 3364), (5673972, 3364),
              (5673984, 3364), (5675560, 3364), (5673971, 3364), (5673985, 3364), (5675558, 3364), (5673986, 3364),
              (5673839, 3364), (5673969, 3364), (5673979, 3364), (5673973, 3364), (5673987, 3364), (5675562, 3364),
              (5673982, 3364), (5675561, 3364), (5675571, 3364), (5673981, 3364), (5675573, 3364), (5675572, 3364),
              (5675580, 3364), (5673970, 3364), (5675569, 3364), (5675559, 3364), (5675574, 3364), (5673980, 3364),
              (5675579, 3364), (5675570, 3364), (5673978, 3364), (5675576, 3364), (5673975, 3364), (5673976, 3364),
              (5675575, 3364), (5675557, 3364), (5673977, 3364), (5673974, 3364), (5675577, 3364), (5676077, 3364),
              (5675555, 3364), (5675556, 3364), (5676076, 3364), (5675565, 3364), (5676075, 3364), (5675563, 3364),
              (5675578, 3364), (5683021, 3364), (5681723, 3364), (5683018, 3364), (5683019, 3364), (5683020, 3364),
              (5613349, 8117), (5613350, 8117), (5708194, 8149), (5641524, 8117), (5565956, 8117), (5591050, 8117),
              (5413266, 8117), (5565212, 8117), (5628291, 8117), (5486202, 8117), (5591049, 8117), (5643219, 8117),
              (5591048, 8117), (5565211, 8117), (5645221, 8117), (5645222, 8117), (5596533, 8117), (5613772, 8117),
              (5637671, 8117), (5596531, 8117), (5637669, 8117), (5596535, 8117), (5637670, 8117), (5645223, 8117),
              (5635883, 8117), (5635884, 8117), (5613370, 8117), (5585835, 8117), (5637668, 8117), (5635885, 8117),
              (5613369, 8117), (5613367, 8117), (5637672, 8117), (5596534, 8117), (5613371, 8117), (5631915, 8117),
              (5596532, 8117), (5708189, 8149), (5708188, 8149), (5708192, 8149), (5708190, 8149), (5486216, 7575),
              (5474702, 7575), (5474701, 7575), (5474703, 7575), (5474705, 7575), (5474707, 7575), (5474704, 7575),
              (5717941, 8149), (5717942, 8149), (5702706, 8149), (5717943, 8149), (5704079, 8149), (1690845, 6868),
              (5758760, 8149), (5460767, 6868), (5460760, 6868), (5461010, 6868), (5474711, 6868), (5460759, 6868),
              (5460763, 6868), (5460764, 6868), (5461011, 6868), (5461009, 6868), (5460768, 6868), (5506460, 3364),
              (5757893, 8149), (5712771, 8117), (5712772, 8117), (5778157, 6868), (5567847, 6868), (5567850, 6868),
              (5567849, 6868), (5567848, 6868), (5641519, 8117), (5686246, 8117), (5647762, 8117), (5532498, 8117),
              (5647763, 8117), (5733352, 8117), (5635882, 8117), (5486232, 8117), (5532501, 8117), (5641522, 8117),
              (5546634, 8117), (5628290, 8117), (5532500, 8117), (5686247, 8117), (5641520, 8117), (5489630, 8117),
              (5670349, 8117), (5532499, 8117), (5685366, 8117), (5791645, 7575), (5782197, 8149), (5791645, 3364),
              (5790777, 8149), (5790779, 8149), (5790780, 8149), (5790781, 8149), (5790778, 8149), (5521177, 3364),
              (1002963, 8149), (1070290, 8149), (1015547, 8149), (5486226, 3364), (5486226, 7575), (5521176, 6868),
              (5486193, 3364), (5852379, 7575), (5486193, 6868), (5852379, 3364), (5665175, 3364), (5301776, 3364),
              (5852378, 6868), (5852377, 6868), (5852376, 6868), (5474712, 6868), (5900571, 8149), (5826979, 8149),
              (5900570, 8149), (5900569, 8149), (5786601, 8149), (5853947, 8149), (5853944, 8149), (5853943, 8149),
              (5853946, 8149), (5884645, 8149), (5853945, 8149), (5897019, 9668), (5897020, 9668), (5897021, 9668),
              (5875181, 6868), (5904416, 8149), (5904415, 8149), (5910165, 8149), (5731172, 9608), (5888312, 9608),
              (5704079, 9608), (5704077, 9608), (5910172, 9608), (5758759, 9608), (5826978, 9608), (5900548, 9608),
              (5900547, 9608), (5910166, 9608), (5910171, 9608), (5826979, 9608), (5790779, 9608), (5910168, 9608),
              (5896692, 9608), (5896693, 9608), (5910175, 9608), (5782197, 9608), (5782065, 9608), (5900570, 9608),
              (5853943, 9608), (5786601, 9608), (5910173, 9608), (5853947, 9608), (5853944, 9608), (5912379, 9608),
              (5910169, 9608), (5910176, 9608), (5910165, 9608), (5884645, 9608), (5731775, 9608), (5910167, 9608),
              (5835401, 9608), (5791047, 9608), (5918531, 8149), (5913733, 9608), (5910166, 8149), (5910173, 8149),
              (5917259, 8149), (5900547, 8149), (5900548, 8149), (5913285, 8149), (5913286, 8149), (5913287, 8149),
              (5913288, 8149), (5782066, 8149), (5921849, 8149)]
    redis_client = get_cluster_client()
    for t in t_list:
        stock_key = gen_stock_key(t[0])
        pre_qty_field = gen_pre_qty_field(t[1])
        print(t, redis_client.hget(stock_key, pre_qty_field))
        redis_client.hdel(stock_key, pre_qty_field)


if __name__ == '__main__':
    # l_read_file("E:/file/download/tt/filter.txt", 500)

    # for s in range(85):
    #     l_read_file("E:/file/download/tt/stock_item_" + str(s + 1) + ".txt", 500)
    #
    # timer_task(10)
    # check_warehouse_qty()
    # item_list = [2481497, 25067509]
    # get_all_stock_list(item_list)
    # get_stock(5698172)
    # ll = [5853947]
    # for i in ll:
    #     delete_stock(i)
    # item_list = [5641519]
    # for i in item_list:
    #     get_stock(i)
    #     # delete_stock(i)
    clear_bmp_pre_qty()
