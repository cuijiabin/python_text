# coding=utf-8
import datetime
import decimal
import json

import util as bm

"""
获取spu的信息然后转换成字典对象
"""


class ExtendJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        return super(ExtendJSONEncoder, self).default(obj)


def get_sql_param(table_name, field, param):
    sql = "SELECT * FROM " + table_name + " WHERE " + field + " IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", param)))
    sql %= condition
    return sql


def get_db_group_info(table_name, field, param):
    cur = bm.get_mia_cursor("db_pop")
    sql = get_sql_param(table_name, field, param)
    cur.execute(sql, param)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def get_mia_group_info(table_name, field, param):
    cur = bm.get_mia_cursor("db_pop")
    sql = get_sql_param(table_name, field, param)
    cur.execute(sql, param)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def get_all_draft(param):
    # spu数据
    spu_data = get_db_group_info("db_pop.item_spu", "id", param)
    spu_ids = list(map(lambda x: x['id'], spu_data))
    print("输出spu")
    print(json.dumps(spu_data, cls=ExtendJSONEncoder))

    # spu草稿数据
    spu_draft_data = get_db_group_info("db_pop.item_spu_draft", "spu_id", spu_ids)
    spu_draft_ids = list(map(lambda x: x['id'], spu_draft_data))
    print("输出spu草稿数据")
    print(json.dumps(spu_draft_data, cls=ExtendJSONEncoder))

    print(spu_data[0].keys() & spu_draft_data[0].keys())
    print(spu_data[0].keys() - spu_draft_data[0].keys())
    print(spu_draft_data[0].keys() - spu_data[0].keys())

    # 商品图片草稿数据
    spu_pictures_draft_data = get_db_group_info("db_pop.item_spu_pictures_draft", "spu_id", spu_draft_ids)
    print("输出商品图片草稿数据")
    print(json.dumps(spu_pictures_draft_data, cls=ExtendJSONEncoder))

    # 规格图片草稿数据
    image_draft_data = get_db_group_info("db_pop.item_specification_image_draft", "spu_id", spu_draft_ids)
    print("输出规格图片草稿数据")
    print(json.dumps(image_draft_data, cls=ExtendJSONEncoder))

    sku_draft_data = get_db_group_info("db_pop.item_sku_draft", "spu_id", spu_draft_ids)
    sku_draft_ids = list(map(lambda x: x['id'], sku_draft_data))
    print("输出sku草稿数据")
    print(json.dumps(sku_draft_data, cls=ExtendJSONEncoder))

    relation_draft_data = get_db_group_info("db_pop.item_sku_specification_relation_draft", "sku_id", sku_draft_ids)
    print("输出sku规格关系草稿数据")
    print(json.dumps(relation_draft_data, cls=ExtendJSONEncoder))

    cost_price_draft_data = get_db_group_info("db_pop.item_cost_price_draft", "spu_id", spu_draft_ids)
    print("输出spu成本价草稿数据")
    print(json.dumps(cost_price_draft_data, cls=ExtendJSONEncoder))

    stock_data = get_db_group_info("db_pop.item_stock", "sku_id", sku_draft_ids)
    print("输出sku库存数据")
    print(json.dumps(stock_data, cls=ExtendJSONEncoder))


def get_all_spu(param):
    # spu数据
    spu_data = get_db_group_info("db_pop.item_spu", "id", param)
    spu_ids = list(map(lambda x: x['id'], spu_data))
    print("输出spu")
    print(json.dumps(spu_data, cls=ExtendJSONEncoder))

    # 商品图片数据
    spu_pictures_data = get_db_group_info("db_pop.item_spu_pictures", "spu_id", spu_ids)
    print("输出商品图片数据")
    print(json.dumps(spu_pictures_data, cls=ExtendJSONEncoder))

    # 规格图片数据
    image_data = get_db_group_info("db_pop.item_specification_image_draft", "spu_id", spu_ids)
    print("输出规格图片数据")
    print(json.dumps(image_data, cls=ExtendJSONEncoder))

    sku_data = get_db_group_info("db_pop.item_sku", "spu_id", spu_ids)
    sku_ids = list(map(lambda x: x['id'], sku_data))
    print("输出sku数据")
    print(json.dumps(sku_data, cls=ExtendJSONEncoder))

    relation_data = get_db_group_info("db_pop.item_sku_specification_relation", "sku_id", sku_ids)
    print("输出sku规格关系数据")
    print(json.dumps(relation_data, cls=ExtendJSONEncoder))

    cost_price_data = get_db_group_info("db_pop.item_cost_price", "spu_id", spu_ids)
    print("输出spu成本价数据")
    print(json.dumps(cost_price_data, cls=ExtendJSONEncoder))

    stock_data = get_db_group_info("db_pop.item_stock", "sku_id", sku_ids)
    print("输出sku库存数据")
    print(json.dumps(stock_data, cls=ExtendJSONEncoder))

    item_ids = list(map(lambda x: x['item_id'], sku_data))
    item_ids = list(set(item_ids))
    item_data = get_mia_group_info("mia_mirror.item", "id", item_ids)
    print("输出item数据")
    print(json.dumps(item_data, cls=ExtendJSONEncoder))
    # print(item_data)


if __name__ == "__main__":
    get_all_spu([101125830])
    # get_all_draft([101125830])
