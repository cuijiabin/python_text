# coding=utf-8
import json

import util as bm
import util.mia_db as mu
from threading import Timer

"""
获取spu的信息然后转换成字典对象
"""


def timed_task(i):
    print("定时输出", str(i))
    i += 1
    Timer(3, timed_task, (i,)).start()


# 获取spuId
def get_db_spu_ids(value_id, is_draft=True):
    cur = bm.get_mia_cursor("db_pop")
    sql = "SELECT spu_id FROM db_pop.item_spu_draft WHERE id = " + str(value_id)
    if is_draft:
        sql = "SELECT id FROM db_pop.item_spu_draft WHERE spu_id = " + str(value_id)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return result_data[0][0]
    return ""


# 获取skuId
def get_db_sku_ids(value_id, is_draft=True):
    cur = bm.get_mia_cursor("db_pop")
    sql = "SELECT id FROM db_pop.item_sku WHERE spu_id = " + str(value_id)
    if is_draft:
        sql = "SELECT id FROM db_pop.item_sku_draft WHERE spu_id = " + str(value_id)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return list(map(lambda x: x[0], result_data))
    return []


# 根据spuId 获取相关id列表
def get_relates_by_spu_id(spu_id):
    spu_draft_id = get_db_spu_ids(spu_id)

    sku_ids = get_db_sku_ids(spu_id, False)
    sku_draft_ids = get_db_sku_ids(spu_draft_id)

    sku_data = mu.get_db_group_info("db_pop.item_sku", "id", sku_ids)
    item_ids = list(map(lambda x: x['item_id'], sku_data))
    item_ids = list(set(item_ids))

    result = dict()
    result["spuId"] = spu_id
    result["spuDraftId"] = spu_draft_id
    result["skuIds"] = sku_ids
    result["skuDraftIds"] = sku_draft_ids
    result["itemIds"] = item_ids

    return result


# 根据spuDraftId 获取相关id列表
def get_relates_by_spu_draft_id(spu_draft_id):
    result = dict()
    sku_draft_ids = get_db_sku_ids(spu_draft_id)
    result["spuDraftId"] = spu_draft_id
    result["skuDraftIds"] = sku_draft_ids
    spu_id = get_db_spu_ids(spu_draft_id, False)
    if not (spu_id is None) and bm.is_number(spu_id):
        sku_ids = get_db_sku_ids(spu_id, False)
        sku_data = mu.get_db_group_info("db_pop.item_sku", "id", sku_ids)
        item_ids = list(map(lambda x: x['item_id'], sku_data))
        item_ids = list(set(item_ids))

        result["spuId"] = spu_id
        result["skuIds"] = sku_ids
        result["itemIds"] = item_ids

    return result


# 根据skuId 获取相关id列表
def get_relates_by_sku_id(sku_id):
    known_data = mu.get_db_group_info("db_pop.item_sku", "id", [sku_id])
    known_data = known_data[0]
    spu_id = known_data["spu_id"]
    spu_draft_id = get_db_spu_ids(spu_id)

    sku_ids = get_db_sku_ids(spu_id, False)
    sku_draft_ids = get_db_sku_ids(spu_draft_id)

    sku_data = mu.get_db_group_info("db_pop.item_sku", "id", sku_ids)
    item_ids = list(map(lambda x: x['item_id'], sku_data))
    item_ids = list(set(item_ids))

    result = dict()
    result["spuId"] = spu_id
    result["spuDraftId"] = spu_draft_id
    result["skuIds"] = sku_ids
    result["skuDraftIds"] = sku_draft_ids
    result["itemIds"] = item_ids

    return result


# 根据skuDraftId 获取相关id列表
def get_relates_by_sku_draft_id(sku_draft_id):
    known_data = mu.get_db_group_info("db_pop.item_sku_draft", "id", [sku_draft_id])
    known_data = known_data[0]
    spu_draft_id = known_data["spu_id"]
    result = dict()
    sku_draft_ids = get_db_sku_ids(spu_draft_id)
    result["spuDraftId"] = spu_draft_id
    result["skuDraftIds"] = sku_draft_ids
    spu_id = get_db_spu_ids(spu_draft_id, False)
    if not (spu_id is None) and bm.is_number(spu_id):
        sku_ids = get_db_sku_ids(spu_id, False)
        sku_data = mu.get_db_group_info("db_pop.item_sku", "id", sku_ids)
        item_ids = list(map(lambda x: x['item_id'], sku_data))
        item_ids = list(set(item_ids))

        result["spuId"] = spu_id
        result["skuIds"] = sku_ids
        result["itemIds"] = item_ids

    return result


# 根据itemId 获取相关id列表
def get_relates_by_item_id(item_id):
    known_data = mu.get_db_group_info("db_pop.item_sku", "item_id", [item_id])
    known_data = known_data[0]
    spu_id = known_data["spu_id"]
    spu_draft_id = get_db_spu_ids(spu_id)

    sku_ids = get_db_sku_ids(spu_id, False)
    sku_draft_ids = get_db_sku_ids(spu_draft_id)

    sku_data = mu.get_db_group_info("db_pop.item_sku", "id", sku_ids)
    item_ids = list(map(lambda x: x['item_id'], sku_data))
    item_ids = list(set(item_ids))

    result = dict()
    result["spuId"] = spu_id
    result["spuDraftId"] = spu_draft_id
    result["skuIds"] = sku_ids
    result["skuDraftIds"] = sku_draft_ids
    result["itemIds"] = item_ids

    return result


def get_all_draft(param):
    # spu数据
    spu_data = mu.get_db_group_info("db_pop.item_spu", "id", param)
    spu_ids = list(map(lambda x: x['id'], spu_data))

    # spu草稿数据
    spu_draft_data = mu.get_db_group_info("db_pop.item_spu_draft", "spu_id", spu_ids)
    spu_draft_ids = list(map(lambda x: x['id'], spu_draft_data))
    print("输出spu草稿数据")
    print(json.dumps(spu_draft_data, cls=bm.ExtendJSONEncoder))

    print(bm.gen_sql("item_spu_draft", spu_draft_data[0]))

    # 商品图片草稿数据
    spu_pictures_draft_data = mu.get_db_group_info("db_pop.item_spu_pictures_draft", "spu_id", spu_draft_ids)
    print("输出商品图片草稿数据")
    print(json.dumps(spu_pictures_draft_data, cls=bm.ExtendJSONEncoder))

    # 规格图片草稿数据
    image_draft_data = mu.get_db_group_info("db_pop.item_specification_image_draft", "spu_id", spu_draft_ids)
    print("输出规格图片草稿数据")
    print(json.dumps(image_draft_data, cls=bm.ExtendJSONEncoder))

    sku_draft_data = mu.get_db_group_info("db_pop.item_sku_draft", "spu_id", spu_draft_ids)
    sku_draft_ids = list(map(lambda x: x['id'], sku_draft_data))
    print("输出sku草稿数据")
    print(json.dumps(sku_draft_data, cls=bm.ExtendJSONEncoder))

    relation_draft_data = mu.get_db_group_info("db_pop.item_sku_specification_relation_draft", "sku_id", sku_draft_ids)
    print("输出sku规格关系草稿数据")
    print(json.dumps(relation_draft_data, cls=bm.ExtendJSONEncoder))

    cost_price_draft_data = mu.get_db_group_info("db_pop.item_cost_price_draft", "spu_id", spu_draft_ids)
    print("输出spu成本价草稿数据")
    print(json.dumps(cost_price_draft_data, cls=bm.ExtendJSONEncoder))

    stock_data = mu.get_db_group_info("db_pop.item_stock", "sku_id", sku_draft_ids)
    print("输出sku库存数据")
    print(json.dumps(stock_data, cls=bm.ExtendJSONEncoder))


def get_all_spu(param):
    # spu数据
    spu_data = mu.get_db_group_info("db_pop.item_spu", "id", param)
    spu_ids = list(map(lambda x: x['id'], spu_data))
    print("输出spu")
    print(json.dumps(spu_data, cls=bm.ExtendJSONEncoder))

    # 商品图片数据
    spu_pictures_data = mu.get_db_group_info("db_pop.item_spu_pictures", "spu_id", spu_ids)
    print("输出商品图片数据")
    print(json.dumps(spu_pictures_data, cls=bm.ExtendJSONEncoder))

    # 规格图片数据
    image_data = mu.get_db_group_info("db_pop.item_specification_image_draft", "spu_id", spu_ids)
    print("输出规格图片数据")
    print(json.dumps(image_data, cls=bm.ExtendJSONEncoder))

    sku_data = mu.get_db_group_info("db_pop.item_sku", "spu_id", spu_ids)
    sku_ids = list(map(lambda x: x['id'], sku_data))
    print("输出sku数据")
    print(json.dumps(sku_data, cls=bm.ExtendJSONEncoder))

    relation_data = mu.get_db_group_info("db_pop.item_sku_specification_relation", "sku_id", sku_ids)
    print("输出sku规格关系数据")
    print(json.dumps(relation_data, cls=bm.ExtendJSONEncoder))

    cost_price_data = mu.get_db_group_info("db_pop.item_cost_price", "spu_id", spu_ids)
    print("输出spu成本价数据")
    print(json.dumps(cost_price_data, cls=bm.ExtendJSONEncoder))

    stock_data = mu.get_db_group_info("db_pop.item_stock", "sku_id", sku_ids)
    print("输出sku库存数据")
    print(json.dumps(stock_data, cls=bm.ExtendJSONEncoder))

    item_ids = list(map(lambda x: x['item_id'], sku_data))
    item_ids = list(set(item_ids))
    item_data = mu.get_mia_group_info("mia_mirror.item", "id", item_ids)
    print("输出item数据")
    print(json.dumps(item_data, cls=bm.ExtendJSONEncoder))


# spu 差异比较
def diff_spu_info(spu_id):
    spu_draft_id = get_db_spu_ids(spu_id)

    spu_data = mu.get_db_group_info("db_pop.item_spu", "id", [spu_id])
    spu_draft_data = mu.get_db_group_info("db_pop.item_spu_draft", "id", [spu_draft_id])

    common_fields = spu_data[0].keys() & spu_draft_data[0].keys()
    formal_fields = spu_data[0].keys() - spu_draft_data[0].keys()
    diff_fields = spu_draft_data[0].keys() - spu_data[0].keys()
    print("公共字段", common_fields)
    print("正式表字段", formal_fields)
    print("草稿表字段", list(diff_fields))

    for field in common_fields:
        if spu_data[0][field] == spu_draft_data[0][field]:
            continue
        print(spu_data[0][field], spu_draft_data[0][field], field, spu_data[0][field] == spu_draft_data[0][field])


# 商品图片比较
def diff_spu_picture_info(spu_id):
    spu_draft_id = get_db_spu_ids(spu_id)

    sku_data = mu.get_db_group_info("db_pop.item_spu_pictures", "spu_id", [spu_id])
    sku_draft_data = mu.get_db_group_info("db_pop.item_spu_pictures_draft", "spu_id", [spu_draft_id])
    print(len(sku_data), len(sku_draft_data))

    common_fields = sku_data[0].keys() & sku_draft_data[0].keys()
    formal_fields = sku_data[0].keys() - sku_draft_data[0].keys()
    diff_fields = sku_draft_data[0].keys() - sku_data[0].keys()

    print("公共字段", common_fields)
    print("正式表字段", formal_fields)
    print("草稿表字段", diff_fields)

    for i in range(len(sku_data)):
        sku = sku_data[i]
        sku_draft = sku_draft_data[i]
        for field in common_fields:
            if sku[field] == sku_draft[field]:
                continue
            print(sku[field], sku_draft[field], field, sku[field] == sku_draft[field])
        print("--------------")


# 规格图片比较
def diff_specification_image_info(spu_id):
    spu_draft_id = get_db_spu_ids(spu_id)

    sku_data = mu.get_db_group_info("db_pop.item_specification_image", "spu_id", [spu_id])
    sku_draft_data = mu.get_db_group_info("db_pop.item_specification_image_draft", "spu_id", [spu_draft_id])
    print(len(sku_data), len(sku_draft_data))

    common_fields = sku_data[0].keys() & sku_draft_data[0].keys()
    formal_fields = sku_data[0].keys() - sku_draft_data[0].keys()
    diff_fields = sku_draft_data[0].keys() - sku_data[0].keys()

    print("公共字段", common_fields)
    print("正式表字段", formal_fields)
    print("草稿表字段", diff_fields)

    for i in range(len(sku_data)):
        sku = sku_data[i]
        sku_draft = sku_draft_data[i]
        for field in common_fields:
            if sku[field] == sku_draft[field]:
                continue
            print(sku[field], sku_draft[field], field, sku[field] == sku_draft[field])
        print("--------------")


# sku 差异比较
def diff_sku_info(spu_id):
    spu_draft_id = get_db_spu_ids(spu_id)
    sku_ids = get_db_sku_ids(spu_id, False)
    sku_draft_ids = get_db_sku_ids(spu_draft_id)

    sku_data = mu.get_db_group_info("db_pop.item_sku", "id", sku_ids)
    sku_draft_data = mu.get_db_group_info("db_pop.item_sku_draft", "id", sku_draft_ids)
    print(len(sku_data), len(sku_draft_data))

    common_fields = sku_data[0].keys() & sku_draft_data[0].keys()
    formal_fields = sku_data[0].keys() - sku_draft_data[0].keys()
    diff_fields = sku_draft_data[0].keys() - sku_data[0].keys()

    print("公共字段", common_fields)
    print("正式表字段", formal_fields)
    print("草稿表字段", diff_fields)

    for i in range(len(sku_data)):
        sku = sku_data[i]
        sku_draft = sku_draft_data[i]
        for field in common_fields:
            if sku[field] == sku_draft[field]:
                continue
            print(sku[field], sku_draft[field], field, sku[field] == sku_draft[field])


# sku 差异比较
def diff_specification_relation_info(spu_id):
    spu_draft_id = get_db_spu_ids(spu_id)
    sku_ids = get_db_sku_ids(spu_id, False)
    sku_draft_ids = get_db_sku_ids(spu_draft_id)

    sku_data = mu.get_db_group_info("db_pop.item_sku_specification_relation", "sku_id", sku_ids)
    sku_draft_data = mu.get_db_group_info("db_pop.item_sku_specification_relation_draft", "sku_id", sku_draft_ids)
    print(len(sku_data), len(sku_draft_data))

    common_fields = sku_data[0].keys() & sku_draft_data[0].keys()
    formal_fields = sku_data[0].keys() - sku_draft_data[0].keys()
    diff_fields = sku_draft_data[0].keys() - sku_data[0].keys()

    print("公共字段", common_fields)
    print("正式表字段", formal_fields)
    print("草稿表字段", diff_fields)

    for i in range(len(sku_data)):
        sku = sku_data[i]
        sku_draft = sku_draft_data[i]
        for field in common_fields:
            if sku[field] == sku_draft[field]:
                continue
            print(sku[field], sku_draft[field], field, sku[field] == sku_draft[field])
        print("--------------")


# 成本价比较
def diff_cost_price_info(spu_id):
    spu_draft_id = get_db_spu_ids(spu_id)

    sku_data = mu.get_db_group_info("db_pop.item_cost_price", "spu_id", [spu_id])
    sku_draft_data = mu.get_db_group_info("db_pop.item_cost_price_draft", "spu_id", [spu_draft_id])
    print(len(sku_data), len(sku_draft_data))

    common_fields = sku_data[0].keys() & sku_draft_data[0].keys()
    formal_fields = sku_data[0].keys() - sku_draft_data[0].keys()
    diff_fields = sku_draft_data[0].keys() - sku_data[0].keys()

    print("公共字段", common_fields)
    print("正式表字段", formal_fields)
    print("草稿表字段", diff_fields)

    for i in range(len(sku_data)):
        sku = sku_data[i]
        sku_draft = sku_draft_data[i]
        for field in common_fields:
            if sku[field] == sku_draft[field]:
                continue
            print(sku[field], sku_draft[field], field, sku[field] == sku_draft[field])
        print("--------------")


def convert_spu(spu_id):
    # spu数据
    spu_data = mu.get_db_group_info("db_pop.item_spu", "id", [spu_id])
    spu_pictures_data = mu.get_db_group_info("db_pop.item_spu_pictures", "spu_id", [spu_id])
    image_data = mu.get_db_group_info("db_pop.item_specification_image_draft", "spu_id", [spu_id])
    sku_data = mu.get_db_group_info("db_pop.item_sku", "spu_id", [spu_id])
    sku_ids = list(map(lambda x: x['id'], sku_data))
    relation_data = mu.get_db_group_info("db_pop.item_sku_specification_relation", "sku_id", sku_ids)
    cost_price_data = mu.get_db_group_info("db_pop.item_cost_price", "spu_id", [spu_id])
    stock_data = mu.get_db_group_info("db_pop.item_stock", "sku_id", sku_ids)
    item_ids = list(map(lambda x: x['item_id'], sku_data))
    item_ids = list(set(item_ids))
    item_data = mu.get_mia_group_info("mia_mirror.item", "id", item_ids)
    stock_item = mu.get_mia_group_info("mia_mirror.stock_item", "item_id", item_ids)

    spu_data = spu_data[0]
    spu_data["pictures_list"] = spu_pictures_data
    spu_data["specification_image_list"] = image_data
    spu_data["sku_list"] = sku_data
    spu_data["specification_relation_list"] = relation_data
    spu_data["cost_price_list"] = cost_price_data
    spu_data["stock_list"] = stock_data
    spu_data["item_list"] = item_data
    spu_data["stock_item"] = stock_item

    return json.dumps(spu_data, cls=bm.ExtendJSONEncoder)


def spu_timed_task(spu_id):
    cur = bm.get_mia_cursor("db_pop")
    sql = "SELECT id FROM db_pop.item_spu WHERE id < " + str(spu_id) + " ORDER BY id DESC LIMIT 1"
    cur.execute(sql)
    result_data = cur.fetchall()
    spu_id = result_data[0][0]
    print(spu_id)
    Timer(3, spu_timed_task, (spu_id,)).start()


if __name__ == "__main__":
    # info = get_relates_by_item_id(2849224)
    # info = get_relates_by_sku_id(2952137)
    info = convert_spu(101204171)
    print(info)
    # get_all_draft([101131232])
    # print(json.dumps(info, cls=bm.ExtendJSONEncoder))
    # spu_timed_task(101126460)
    # timed_task(10)
    # print(bm.camel_convert("crm_strategy_task_dependency", "_"))
    #
    # TODO 库存信息的查询功能
