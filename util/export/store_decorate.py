"""
店铺装修
"""

# coding=utf-8
import common_build_model as bm


# 获取mia主库供应商的基本信息
def get_pop_supplier_map(column=["distinct d.store_id", "d.templete_id", "d.supplier_id"]):
    cur = bm.get_mia_cursor()
    # column = ", ".join(list(map(lambda x: x, column)))
    # sql = "SELECT " + column + " FROM db_pop.store_decoration d WHERE d.type_id !=3 and d.supplier_id not in (SELECT t.supplier_id from db_pop.store_decoration t where t.type_id = 3)"

    sql = "SELECT t.id as sku, pxu.daily_price as '当前销售价'FROM item t left join customer_supplier a on t.supplier_id = a.id LEFT JOIN stock_warehouse b ON t.supplier_id = b.supplier_id LEFT JOIN procurement_contract c on t.supplier_id = c.supplier_id LEFT JOIN item_daily_price    pxu on t.id = pxu.sku WHERE a.pop_admin_id IN (SELECT user_id FROM sec_user_dep_map WHERE department_id IN (67,130) )and b.type in (3,5,7,10,11,12,13) and c.`status` = 2 and t.item_multiple_score >=3 and t.item_multiple_score <= 5 and t.status in (0,1) and pxu.start_time < NOW() and (pxu.end_time > NOW() or pxu.end_time = '0000-00-00 00:00:00')";
    cur.execute(sql)
    f_data = cur.fetchall()

    # 转成列表对象
    # f_data = list(map(lambda x: {"store_id": x[0], "templete_id": x[1], "supplier_id": x[2]}, f_data))
    # result = {}
    merfile = open("F:/project_dir/merge2.txt", "a", encoding="utf8")
    for sup in f_data:
        merfile.write(str(sup))
        merfile.write('\n')

    merfile.close()
    return


if __name__ == "__main__":
    get_pop_supplier_map()
