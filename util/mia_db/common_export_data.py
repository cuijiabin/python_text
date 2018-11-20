# coding=utf-8
import util as bm
import xlrd

"""
通用数据导出文件系统
https://github.com/coleifer/peewee 参考orm


"""

"""
select distinct id from mia_mirror.customer_supplier where
pop_admin_id in(select user_id from mia_mirror.sec_user_dep_map where department_id in
                (select department_id from mia_mirror.hr_department where parent_id = 55))

TODO 下一步工作 把sql做成配置文件
"""


# TODO SELECT id, mia_supplier_id,name,business_id_ng, supplier_admin_id FROM vr_pop.pop_customer_supplier
# TODO SELECT name FROM vr_pop.pop_customer_supplier


def get_pop_supplier():
    # TODO 获取pop供应商相关情况
    pass


# 获取mia主库供应商的基本信息
def get_pop_supplier_map(args, column=["p.id", "p.mia_supplier_id", "p.pop_admin_id"]):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, column)))
    sql = "SELECT " + column + " FROM vr_pop.pop_customer_supplier p WHERE p.mia_supplier_id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(map(lambda x: {"pop_supplier_id": x[0], "mia_supplier_id": x[1], "pop_admin_id": x[2]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["mia_supplier_id"], sup)
    return result


# 获取mia主库供应商的基本信息
def get_supplier_map(args, column=["c.id", "c.name", "c.pop_admin_id", "s.name", "sw.type", "sw.id"]):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, column)))
    sql = "SELECT " + column + " FROM mia_mirror.customer_supplier c " \
                               "left join mia_mirror.stock_warehouse sw on c.id = sw.supplier_id " \
                               "left join mia_mirror.sec_user s on  " \
                               "c.pop_admin_id = s.user_id WHERE c.id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(
        map(lambda x: {"id": x[0], "name": x[1], "pop_admin_id": x[2], "user_name": x[3], "w_type": x[4], "w_id": x[5]},
            f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["id"], sup)
    return result


# 获取vr_pop 供应商的品牌还有最新分类
def get_supplier_brand(args):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, ["supplier_id", "brand_id", "category_id_ng"])))
    sql = "SELECT " + column + " FROM vr_pop.pop_supplier_brand WHERE supplier_id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()
    f_data = list(map(lambda x: {"supplier_id": x[0], "brand_id": x[1], "category_id_ng": x[2]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["id"], sup)
    return result


# 获取mia主库品牌名称
def get_brand_map(args):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, ["id", "name"])))
    sql = "SELECT " + column + " FROM mia_mirror.item_brand WHERE id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(map(lambda x: {"id": x[0], "name": x[1]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["id"], sup["name"])
    return result


# 获取mia主库分类名称
def get_category_map(args):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, ["id", "name"])))
    sql = "SELECT " + column + " FROM mia_mirror.item_category_ng WHERE id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(map(lambda x: {"id": x[0], "name": x[1]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["id"], sup["name"])
    return result


# TODO select s.name as uname, d.name as dname FROM mia_mirror.sec_user s
# inner join mia_mirror.hr_department d on s.department_id = d.department_id
# where s.user_id =

# TODO select status from mia_mirror.partner_login where supplier_id =


# 获取mia系统用户名称
def get_sec_user_map(args):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, ["user_id", "name"])))
    sql = "SELECT " + column + " FROM mia_mirror.sec_user WHERE user_id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(map(lambda x: {"user_id": x[0], "name": x[1]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["user_id"], sup["name"])
    return result


# 获取商家店铺图片
def get_store_pic():
    # SELECT logo_url FROM popTest.store_draft   WHERE supplier_id =  1231  AND logo_url IS NOT NULL ORDER BY modify_time DESC LIMIT 1
    pass


# 获取vr_pop合同号
def get_contractno_map(args):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, ["supplier_id", "contract_no", "status"])))
    sql = "SELECT " + column + " FROM vr_pop.procurement_contract WHERE supplier_id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(map(lambda x: {"supplier_id": x[0], "contract_no": x[1], "status": x[2]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["supplier_id"], sup)
    return result


# 获取mia商品
def get_item_supplier_map(args):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, ["id", "supplier_id", "warehouse_type", "status"])))
    sql = "SELECT " + column + " FROM mia_mirror.item WHERE id IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(map(lambda x: {"id": x[0], "supplier_id": x[1], "warehouse_type": x[2], "status": x[3]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["id"], sup)
    return result


def getKdRate(contractNo, brandId):
    cur = bm.get_mia_cursor()
    cur.execute("select kd_rate from mia_mirror.contract_brand_kd_rate_cycle "
                "where contract_no = %s "
                "and brand_id = " + str(brandId) + " and status = 1 "
                                                   "and NOW() BETWEEN start_date and end_date", str(contractNo))
    data = cur.fetchall()
    if data and len(data) > 0:
        return data[0][0]
    cur.execute("select kd_rate from mia_mirror.contract_brand_kd_rate "
                "where contract_no = %s "
                "and brand_id = " + str(brandId), str(contractNo))
    data = cur.fetchall()
    if data and len(data) > 0:
        return data[0][0]
    return ""


def get_warehouse_id(item_id):
    cur = bm.get_mia_cursor()
    cur.execute("select sw.id as warehouse_id from mia_mirror.customer_supplier cs "
                "left join mia_mirror.stock_warehouse sw on cs.id = sw.supplier_id where cs.id"
                " = (SELECT supplier_id FROM mia_mirror.item where id = " + item_id + ")")
    data = cur.fetchall()
    if data and len(data) > 0:
        return data[0][0]
    return ""


def get_stock_item_id(item_id, item_size, warehouse_id, stock_quantity):
    cur = bm.get_mia_cursor()
    cur.execute("SELECT id as stock_item_id, stock_quantity FROM mia_mirror.stock_item "
                "where item_id = " + item_id + " and item_size = '" + item_size
                + "' and warehouse_id = " + warehouse_id
                + " and status = 1 and stock_quantity >=" + stock_quantity)
    data = cur.fetchall()
    if data and len(data) > 0:
        return data[0]
    return ""


def get_store_map(args):
    cur = bm.get_mia_cursor()
    column = ", ".join(list(map(lambda x: x, ["id", "supplier_id", "name", "status"])))
    sql = "SELECT " + column + " FROM db_pop.store_info WHERE supplier_id IN (%s) and status = 1"
    condition = ", ".join(list(map(lambda x: "%s", args)))
    sql %= condition

    cur.execute(sql, args)
    f_data = cur.fetchall()

    # 转成列表对象
    f_data = list(map(lambda x: {"id": x[0], "supplier_id": x[1], "name": x[2], "status": x[3]}, f_data))
    result = {}
    for sup in f_data:
        result.setdefault(sup["supplier_id"], sup)
    return result


"""
根据商家id列表获取商家

python 字符串，元组， 列表，字典之间的转换
http://www.cnblogs.com/tobeprogramer/p/3982417.html

关于一些重要问题的描述：

11:23 暂时先放弃一下数据
14:18 暂时算是完成结果了
"""


def mergeDict():
    list1 = ['key1', 'key2', 'key3']
    list2 = ['1', '2', '3']
    list = dict(zip(list1, list2))
    print(list)

    new_list = [['key1', 'value1'], ['key2', 'value2'], ['key3', 'value3']]
    print(dict(new_list))


def open_excel(file):
    try:
        f_data = xlrd.open_workbook(file)
        return f_data
    except Exception as e:
        print(str(e))


def get_pic():
    with open("E:/File/download/444.txt", encoding="utf8") as f:
        line = f.readline()
        cur = bm.get_mia_cursor()
        index = 0
        while line:
            line = line.strip('\n').split()[0]
            line = line[19:]
            # m = line.rfind(".") + 1
            # print(line, line[m:])
            # TODO 开始进行图片的查询了！
            # cur.execute("SELECT spu_id FROM db_pop.item_specification_image where spec_image_url like '%"+line+"%'")
            # data = cur.fetchall()
            # if data and len(data) > 0:
            #     print(data[0][0])
            cur.execute("SELECT item_id FROM mia_mirror.item_pictures where local_url = '" + line + "'")
            data = cur.fetchall()
            if data and len(data) > 0:
                print(data[0][0], line)

            index += 1
            print(index)

            line = f.readline()
        f.close()


if __name__ == "__main__":
    # 供应商id（主库id），供应商名称，商家主营类目，品牌id，品牌名称，品牌主营类目，招商负责人id，招商负责人名称（pop库招商负责人）品牌扣点 stock_warehouse
    # 0.查询所有供应商id  select distinct supplier_id from stock_warehouse where type = 7 order by supplier_id;mia 共有100个
    # 1.查询仓库类型为7的供应商 SELECT mia_supplier_id,name,business_id_ng, supplier_admin_id FROM vr_pop.pop_customer_supplier where id = 175;vr_pop
    # 2.查询品牌id SELECT brand_id, category_id_ng FROM vr_pop.pop_supplier_brand where supplier_id = 175;vr_pop
    # 2.商家主营类目id select name from item_category_ng where id = 10023;mia
    # 3.查询品牌名称 select name from item_brand where id = 422;mia
    # 4.查询招商负责人 select name from sec_user where user_id = 12380;mia
    # 查询合同编号 select contract_no from vr_pop.procurement_contract where pop_supplier_id = 175;vr_pop
    # 5.扣点信息 select kd_rate from contract_brand_kd_rate_cycle limit 10; select kd_rate from contract_brand_kd_rate; mia 根据什么来查询呢？
    # select * from contract_brand_kd_rate_cycle where contract_no = 'CT-175-20141001' and brand_id = 422 and `status` = 1 and NOW() BETWEEN start_date and end_date;
    # select * from contract_brand_kd_rate where contract_no = 'CT-175-20141001' and brand_id = 422
    # convert()
    # getKdRate("CT-468-20150201", 468)
    sm = []

    mm = []
    with open("E:/work-text/log.txt") as of:
        line = of.readline()
        while line:
            line = line.strip('\n')
            mm.append(line)
            line = of.readline()
        of.close()
    mp = get_supplier_map(mm)

    htmap = {
        - 1: '作废',
        1: '未开始',
        2: '执行中',
        3: '过期',
        4: '品类审核意见',
        5: '部门负责人审核意见',
        11: '财务审核一级意见',
        12: '财务审核二级意见',
        13: '财务审核三级意见',
        14: '法务审核意见',
        6: 'ceo审核意见',
        7: '已驳回',
        8: '已撤销',
        9: '冻结',
        10: '草稿'
    }

    itmap = {
        - 1: '作废',
        0: '售罄',
        1: '上线',
        2: '待上线',
        3: '下线',
        4: '战略储藏'
    }

    csmap = {
        3: "国内",
        5: "直邮",
        7: "保税区"
    }
    # print(mp)
    print("商家类型（直邮，保税区）")
    for i in mm:
        try:
            # print(htmap[mp[int(i)]["status"]])
            print(mp[int(i)]["user_name"])
            # print(mp[int(i)])
        except Exception as e:
            print("")
