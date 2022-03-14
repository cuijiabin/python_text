# coding=utf-8
from string import Template


# 通过Template生成文本 mysql通过concat函数也可以生成
def gen_txt_by_tpl():
    sql_tmp = Template(
        "SELECT * from brand_stock_item_channel WHERE channel_id = $channel_id and item_id = $item_id "
        "AND tz_item_id = $tz_item_id ;")
    sql = sql_tmp.substitute(channel_id=220, item_id=1234, tz_item_id=66)
    print(sql)

    code_list = [1, 2, 3, 4, 5]
    code_list = list(map(lambda x: "'" + str(x) + "'", code_list))
    code_list = ','.join(code_list)
    sql_tmp = Template(
        "select id,order_code,`status`,wdgj_status,oms_sync_status,warehouse_id,channel,brand_channel "
        "from orders WHERE order_code IN ($code_list) ;")
    sql = sql_tmp.substitute(code_list=code_list)
    print(sql)


def gen_txt_by_concat():
    sql = "select id,item_id,warehouse_id from stock_item where item_id in (%s);"
    item_ids = [1, 2, 3, 4, 5]
    condition = ", ".join(list(map(lambda x: str(x), item_ids)))
    sql %= condition

    print(sql)


if __name__ == '__main__':
    gen_txt_by_tpl()
    gen_txt_by_concat()
