# coding=utf-8
import common_excel as ce
import common_export_data as cd
import datetime
from matplotlib.dates import num2date

"""
秒杀活动锁定库存
"""


# 格式化Excel中的日期
def re_date(date):
    __startDt = datetime.date(1899, 12, 31).toordinal() - 1
    if type(date) == float:
        return num2date(__startDt + date).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return date.strip("")


# excel文件格式化处理
def handel_promotion(p_list):
    for p in p_list:
        p["start_time"] = re_date(p["start_time"])
        p["end_time"] = re_date(p["end_time"])
        p["ums_id"] = int(p["ums_id"]) if type(p["ums_id"]) is float else p["ums_id"]
        p["ums_id"] = str(p["ums_id"])
        p["item_id"] = int(p["item_id"]) if type(p["item_id"]) is float else p["item_id"]
        p["item_id"] = str(p["item_id"])
        p["limit_stock"] = int(p["limit_stock"]) if type(p["limit_stock"]) is float else p["limit_stock"]
        p["limit_stock"] = str(p["limit_stock"])


# 生成sql
def gen_sql(p_list):
    for p in p_list:
        warehouse_id = cd.get_warehouse_id(p["item_id"])
        if warehouse_id == "":
            p["is_right"] = 1
            p["reason"] = "找不到仓库id"
            continue

        warehouse_id = str(warehouse_id)
        mmm = cd.get_stock_item_id(p["item_id"], p["item_size"], warehouse_id, p["limit_stock"])
        if mmm == "":
            mmm = (0, 0)

        stock_item_id = mmm[0]

        if stock_item_id == "":
            p["is_right"] = 2
            p["reason"] = "找不到stock_item_id"
            continue

        stock_item_id = str(stock_item_id)
        sql = "INSERT INTO `mia_promotion_limit_stock` (ums_id, item_id, stock_item_id, limit_stock, item_size, start_time, end_time) " \
              "VALUES (%s, %s, %s, %s, '%s', '%s', '%s');"
        sql %= (
            p["ums_id"], p["item_id"],stock_item_id, p["limit_stock"], p["item_size"], "2017-05-22 19:50:00", "2017-05-23 19:50:00")

        stock_sql = "UPDATE stock_item SET stock_quantity = (stock_quantity-%d) WHERE id = %s;"
        stock_sql %= (int(p["limit_stock"]), stock_item_id)
        print(stock_sql)
        print(sql)
        p["is_right"] = 0

        # print(p["ums_id"], p["item_id"], p["item_size"], mmm[1],stock_item_id)

    print("\n")
    for rp in p_list:
        print(rp)
        # if 0 == rp["is_right"]:
        #     print(rp, "处理失败", rp["reason"])



if __name__ == "__main__":
    # 1.解析读取excel模板
    excel_title = ["ums_id", "item_id", "item_size", "limit_stock", "start_time", "end_time"]
    promotion_list = ce.read_excel_array("E:/File/download/pop锁定库存模板.xlsx", 0, 1, excel_title)
    handel_promotion(promotion_list)
    gen_sql(promotion_list)
