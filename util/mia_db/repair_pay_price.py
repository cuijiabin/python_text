# coding=utf-8
import re
from itertools import groupby
from string import Template

import xlrd
import util as bm


def get_order_list(superior_order_code):
    cur = bm.get_mia_cursor("mia_mirror")
    sql_tmp = Template(
        "SELECT id,sale_price,deal_price,pay_price from orders "
        "WHERE superior_order_code = '$superior_order_code' and warehouse_id = 8149"
    )
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    result = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return result


def get_order_item_list(superior_order_code):
    cur = bm.get_mia_cursor("mia_mirror")
    sql_tmp = Template(
        "SELECT id,order_id,sale_price,deal_price,pay_price,promotion_info, "
        "item_id,spu_id,promotion_id,promotion_type,pro_discount "
        "from order_item WHERE order_id IN( "
        "SELECT id from orders "
        "WHERE superior_order_code = '$superior_order_code' and warehouse_id = 8149)"
    )
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    result = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return result


def get_update_sql(superior_order_code):
    order_list = get_order_list(superior_order_code)
    order_item_list = get_order_item_list(superior_order_code)
    print("-- 父单号" + superior_order_code + "修改")
    order_dict = dict((o["id"], o) for o in order_list)
    print(order_dict)
    # order_item_dict = dict((o["item_id"], o) for o in order_item_list)
    # print(order_item_dict)

    for k, g in groupby(order_item_list, lambda x: x["item_id"]):
        print(k)
        print(len(list(g)))


def judge_order(order_code_list):
    cur = bm.get_mia_cursor("mia_mirror")
    sql_tmp = Template(
        "SELECT o.order_code,oi.item_id,count(oi.qty) as num,i.brand_id "
        "from order_item oi INNER JOIN orders o on oi.order_id = o.id "
        "INNER JOIN item i on oi.item_id = i.id "
        "WHERE o.order_code in ($order_code_list) "
        "and oi.item_id not in (2474253, 2474252, 2474245, 5486224, 2474219, 5486225, 2474190, 2506747, 2734559, "
        "4548492, 5096238, 5096239, 5096240, 5096241, 5096234, 5096235, 5096236, 5096237, 5502653, 5502654, "
        "5502655, 5502656, 5502657, 5502650, 5502651, 5502652, 5917239, 5917240, 5917241, 5917242, 5917243, "
        "5917249, 5917250, 5917251, 5917252) "
        "GROUP BY oi.order_id,oi.item_id"
    )
    sql = sql_tmp.substitute(order_code_list=','.join(map(lambda x: "'" + x + "'", order_code_list)))
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    result = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    rm = dict()
    for i in result:
        pre = rm.get(i["order_code"])
        if pre is None:
            rm[i["order_code"]] = i
        elif i['brand_id'] != 6769:
            rm[i["order_code"]] = i

    for o in order_code_list:
        r = rm.get(o)
        if r is None:
            print("无#无")
        else:
            if r['brand_id'] == 6769:
                print("有#无")
            else:
                print("有#有")
    return


# 重置预占库存
if __name__ == '__main__':
    data = xlrd.open_workbook("E:\\file\\download\\模板数据.xlsx")
    # 2.获取一个工作表
    table = data.sheets()[5]
    # 3.获取行数与列数
    row_num = table.nrows
    col_num = table.ncols
    print("这个工作表的行数是：" + str(row_num) + "；行数是：" + str(col_num))
    # 4.输出栏目信息
    columns = table.row_values(0)
    print(columns)
    rule = re.compile(r'[a-zA-z]')

    tables = []
    order_code_list = []
    last_num = row_num - 1
    for i in range(1, row_num):
        row_value = table.row_values(i)
        order_code_list.append(row_value[1])
        if (i % 1000 == 0) or (i == last_num):
            judge_order(order_code_list)
            order_code_list = []

    # judge_order(['2102012410183832', '2102012410184530', '2102012410184540', '2101062405394253'])
