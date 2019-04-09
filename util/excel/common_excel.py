# coding=utf-8
import traceback
import util as bm
import xlrd

"""
1.引用之前默写的各种小的工具类 主要就是文件名称 build_model 但是目前IDE是有这个bug的
2.主要的Excel处理工具

return_items
new_refund_request
3.问题：特殊类型字段的处理 写入新的Excel？
a.数字类型的变量 最后补充了一个0 这个要如何来处理？
b.对于日期类型的变量要怎么来处理呢？[2种方式]
xlrd.xldate_as_tuple(table.cell(2,2).value, 0)   #转化为元组形式
xlrd.xldate.xldate_as_datetime(table.cell(2,2).value, 1)   #直接转化为datetime对象

下一步问题的处理 关于excel的写入的各种问题
"""

rule_set_map = {
    '包邮发': '2',
    '加收10元': '3'
}
rule_amount_map = {
    '包邮发': 0,
    '加收10元': 10
}

rrule_set_map = {
    '不发/加收30元': '1,3',
    '不发/加收60元': '1,3',
    '不发/加收80元': '1,3',
    '加收100元': '3',
    '不发货/加收20元': '1,3',
    '不发/加收20元': '1,3',
    '不发/包邮发': '1,2',
    '不发/加收15元': '1,3',
    '包邮发': '2',
    '不发/加收50元': '1,3',
    '加收20元': '3',
    '加收10元': '3',
    '不发/加收130元': '1,3',
    '加收30元': '3',
    '不发/加收35元': '1,3',
    '不发货': '1',
    '加收50元': '3',
    '加收80元发普通快递80,EMS60元顺丰200': '3',
    '不发': '1',
    '不发/加收200元': '1,3',
    '不发/加收10元': '1,3',
    '不发/加收100元': '1,3',
    '加收300元': '3',
    '加收120元': '3'
}
rrule_amount_map = {
    '不发/加收30元': 30,
    '不发/加收60元': 60,
    '不发/加收80元': 80,
    '加收100元': 100,
    '不发货/加收20元': 20,
    '不发/加收20元': 20,
    '不发/包邮发': 0,
    '不发/加收15元': 15,
    '包邮发': 0,
    '不发/加收50元': 50,
    '加收20元': 20,
    '加收10元': 10,
    '不发/加收130元': 130,
    '加收30元': 30,
    '不发/加收35元': 35,
    '不发货': 0,
    '加收50元': 50,
    '加收80元发普通快递80,EMS60元顺丰200': 200,
    '不发': 0,
    '不发/加收200元': 200,
    '不发/加收10元': 10,
    '不发/加收100元': 100,
    '加收300元': 300,
    '加收120元': 120,
}


# 打开excel文件
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except FileNotFoundError:
        print("文件%s 不存在" % file)
        return None
    except Exception as e:
        print("str(Exception):\t", str(Exception))
        print("str(e):\t\t", str(e))
        print("repr(e):\t", repr(e))
        print("e.message:\t", e.message)
        print("traceback.print_exc():\t", traceback.print_exc())
        print("traceback.format_exc():\n%s" % traceback.format_exc())


# 遍历读取Excel内容
def read_normal_excel(file_path, idx=0, assign=[], pre_num=0):
    data = open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[idx]
    row_num = sheets.nrows
    col_num = sheets.ncols

    value_list = []
    if pre_num > 0:
        row_num = pre_num
    for i in range(2, row_num):
        row_value = sheets.row_values(i)
        if assign is not None and len(assign) > 0:
            for j in assign:
                cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
                print(cell_value, end=" ")
        else:
            row_param = []
            for j in range(0, col_num):
                cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
                if j == 0:
                    cell_value = cell_value.split("》")[-1]
                elif j == 9:
                    if cell_value == "按单加收":
                        cell_value = 2
                    else:
                        cell_value = 2
                elif j > 1:
                    value_list.append(cell_value)
                row_param.append(cell_value)

            print(gen_rule_sql(i - 1, row_param[0], row_param[1], row_param[9]))
            # 新疆31、西藏26
            print(gen_rule_prov_sql(i - 1, 31, rule_set_map[row_param[2]], rule_amount_map[row_param[2]]))
            print(gen_rule_prov_sql(i - 1, 26, rule_set_map[row_param[2]], rule_amount_map[row_param[2]]))
            # 内蒙古11、青海29、宁夏30、甘肃28
            print(gen_rule_prov_sql(i - 1, 11, rule_set_map[row_param[3]], rule_amount_map[row_param[3]]))
            print(gen_rule_prov_sql(i - 1, 29, rule_set_map[row_param[3]], rule_amount_map[row_param[3]]))
            print(gen_rule_prov_sql(i - 1, 30, rule_set_map[row_param[3]], rule_amount_map[row_param[3]]))
            print(gen_rule_prov_sql(i - 1, 28, rule_set_map[row_param[3]], rule_amount_map[row_param[3]]))
            # 海南23
            print(gen_rule_prov_sql(i - 1, 23, rule_set_map[row_param[4]], rule_amount_map[row_param[4]]))
            # 辽宁8
            print(gen_rule_prov_sql(i - 1, 8, rule_set_map[row_param[5]], rule_amount_map[row_param[5]]))
            # 吉林9
            print(gen_rule_prov_sql(i - 1, 9, rule_set_map[row_param[6]], rule_amount_map[row_param[6]]))
            # 黑龙江10
            print(gen_rule_prov_sql(i - 1, 10, rule_set_map[row_param[7]], rule_amount_map[row_param[7]]))

        # print("\n")
    # value_list = list(set(value_list))
    # print(value_list)


# 遍历读取Excel内容
def read_first_excel(file_path, idx=0, assign=[], pre_num=0):
    data = open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[idx]
    row_num = sheets.nrows
    col_num = sheets.ncols

    value_list = []
    if pre_num > 0:
        row_num = pre_num
    for i in range(2, row_num):
        row_value = sheets.row_values(i)
        if assign is not None and len(assign) > 0:
            for j in assign:
                cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
                print(cell_value, end=" ")
        else:
            row_param = []
            for j in range(0, col_num):
                cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
                if j == 0:
                    cell_value = cell_value.split("》")[-1]
                elif j == 9:
                    if cell_value == "按单加收":
                        cell_value = 2
                    else:
                        cell_value = 2
                elif j > 1:
                    value_list.append(cell_value)
                row_param.append(cell_value)

            print(gen_rule_sql(i + 2530, row_param[0], row_param[1], row_param[9]))
            # 新疆31、西藏26
            print(gen_rule_prov_sql(i + 2530, 31, rrule_set_map[row_param[2]], rrule_amount_map[row_param[2]]))
            print(gen_rule_prov_sql(i + 2530, 26, rrule_set_map[row_param[2]], rrule_amount_map[row_param[2]]))
            # 内蒙古11、青海29、宁夏30、甘肃28
            print(gen_rule_prov_sql(i + 2530, 11, rrule_set_map[row_param[3]], rrule_amount_map[row_param[3]]))
            print(gen_rule_prov_sql(i + 2530, 29, rrule_set_map[row_param[3]], rrule_amount_map[row_param[3]]))
            print(gen_rule_prov_sql(i + 2530, 30, rrule_set_map[row_param[3]], rrule_amount_map[row_param[3]]))
            print(gen_rule_prov_sql(i + 2530, 28, rrule_set_map[row_param[3]], rrule_amount_map[row_param[3]]))
            # 海南23
            print(gen_rule_prov_sql(i + 2530, 23, rrule_set_map[row_param[4]], rrule_amount_map[row_param[4]]))
            # 辽宁8
            print(gen_rule_prov_sql(i + 2530, 8, rrule_set_map[row_param[5]], rrule_amount_map[row_param[5]]))
            # 吉林9
            print(gen_rule_prov_sql(i + 2530, 9, rrule_set_map[row_param[6]], rrule_amount_map[row_param[6]]))
            # 黑龙江10
            print(gen_rule_prov_sql(i + 2530, 10, rrule_set_map[row_param[7]], rrule_amount_map[row_param[7]]))

    # value_list = list(set(value_list))
    # print(value_list)


def read_third_excel(file_path, idx=0, assign=[], pre_num=0):
    data = open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[idx]
    row_num = sheets.nrows
    col_num = sheets.ncols

    if pre_num > 0:
        row_num = pre_num
    k = 3008
    for i in range(1, row_num):
        row_value = sheets.row_values(i)
        if assign is not None and len(assign) > 0:
            for j in assign:
                cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
                print(cell_value, end=" ")
        else:
            row_param = []
            for j in range(0, col_num):
                cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
                if j == 0:
                    cell_value = cell_value.split("》")[-1]
                row_param.append(cell_value)

            freight_rule_id = get_freight_rule_id(row_param[1])
            if freight_rule_id != "":
                # 贵州24、云南25
                print(gen_rule_prov_sql(freight_rule_id, 24, "1,3", 10))
                print(gen_rule_prov_sql(freight_rule_id, 25, "1,3", 10))
            else:
                print(gen_rule_sql(k, row_param[0], row_param[1], 2))
                # 贵州24、云南25
                print(gen_rule_prov_sql(k, 24, "1,3", 10))
                print(gen_rule_prov_sql(k, 25, "1,3", 10))
                k += 1


def gen_rule_sql(rule_id, rule_name, category_id_ng, rule_type):
    return "INSERT INTO freight_rule(id, rule_name, category_id_ng, type) VALUES ({rule_id},'{rule_name}', {category_id_ng}, {rule_type});".format(
        rule_id=rule_id, rule_name=rule_name, category_id_ng=category_id_ng, rule_type=rule_type)


def gen_rule_prov_sql(freight_rule_id, prov_id, rule_set, freight_amount):
    return "INSERT INTO freight_rule_prov(freight_rule_id, prov_id, rule_set, freight_amount) VALUES({freight_rule_id},{prov_id}, '{rule_set}', {freight_amount});".format(
        freight_rule_id=freight_rule_id, prov_id=prov_id, rule_set=rule_set, freight_amount=freight_amount)


# 获取spuId
def get_freight_rule_id(value_id):
    cur = bm.get_mia_test_cursor("mia_test2")
    sql = "SELECT id FROM freight_rule WHERE category_id_ng = " + str(value_id)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return result_data[0][0]
    return ""


if __name__ == "__main__":
    # id 15507 (新疆31、西藏26)加收10元运费 (内蒙古11、青海29、宁夏30、甘肃28)包邮发 (海南23)包邮发 (辽宁8)包邮发 (吉林9)包邮发 (黑龙江10)包邮发 (其他区域)包邮发 (收取单位)按单加收
    read_third_excel("F:/File/download/分类规则汇总_全分类.xlsx", 2, None, 0)
