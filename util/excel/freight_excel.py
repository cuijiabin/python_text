# coding=utf-8
import util as bm

"""
1.优先处理第一种情况
2.第二种的时候避开第一种情况
3.保存1与2后处理情况3
"""


# 栏目去重
def duplicate_remove(file_path, idx=0, start_num=0, default_value=0):
    data = bm.open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[idx]
    value_list = []
    for i in range(start_num, sheets.nrows):
        row_value = sheets.row_values(i)
        for j in range(0, sheets.ncols):
            cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
            if j > 1:
                value_list.append(cell_value)
    value_list = list(set(value_list))
    default_list = [default_value for n in range(len(value_list))]
    print(dict(zip(value_list, default_list)))


# 生成特殊分类sql
def read_keynote_excel(file_path, start_num=2, limit_num=500, set_map={}, amount_map={}, start_id=1):
    data = bm.open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[0]
    row_num = (start_num + limit_num) if (start_num + limit_num) < sheets.nrows else sheets.nrows
    for i in range(start_num, row_num):
        row_value = sheets.row_values(i)
        row_param = []
        for j in range(0, sheets.ncols):
            cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
            if j == 0:
                cell_value = cell_value.split("》")[-1]
            elif j == 9:
                if cell_value == "按单加收":
                    cell_value = 2
                else:
                    cell_value = 1

            row_param.append(cell_value)

        print(gen_rule_sql(start_id, row_param[0], row_param[1], row_param[9]))
        # 新疆31、西藏26
        print(gen_rule_prov_sql(start_id, 31, set_map[row_param[2]], amount_map[row_param[2]]))
        print(gen_rule_prov_sql(start_id, 26, set_map[row_param[2]], amount_map[row_param[2]]))
        # 内蒙古11、青海29、宁夏30、甘肃28
        print(gen_rule_prov_sql(start_id, 11, set_map[row_param[3]], amount_map[row_param[3]]))
        print(gen_rule_prov_sql(start_id, 29, set_map[row_param[3]], amount_map[row_param[3]]))
        print(gen_rule_prov_sql(start_id, 30, set_map[row_param[3]], amount_map[row_param[3]]))
        print(gen_rule_prov_sql(start_id, 28, set_map[row_param[3]], amount_map[row_param[3]]))
        # 海南23
        print(gen_rule_prov_sql(start_id, 23, set_map[row_param[4]], amount_map[row_param[4]]))
        # 辽宁8
        print(gen_rule_prov_sql(start_id, 8, set_map[row_param[5]], amount_map[row_param[5]]))
        # 吉林9
        print(gen_rule_prov_sql(start_id, 9, set_map[row_param[6]], amount_map[row_param[6]]))
        # 黑龙江10
        print(gen_rule_prov_sql(start_id, 10, set_map[row_param[7]], amount_map[row_param[7]]))
        start_id += 1


# 生成普通分类sql
def read_common_excel(file_path, start_num=2, limit_num=500, set_map={}, amount_map={}, default_id=1):
    data = bm.open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[1]
    row_num = (start_num + limit_num) if (start_num + limit_num) < sheets.nrows else sheets.nrows

    myfile = open("F:/File/download/t2.txt", 'a', encoding="utf8")

    for i in range(start_num, row_num):
        row_value = sheets.row_values(i)
        row_param = []
        for j in range(0, sheets.ncols):
            cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
            if j == 0:
                cell_value = cell_value.split("》")[-1]
            elif j == 9:
                if cell_value == "按单加收":
                    cell_value = 2
                else:
                    cell_value = 1

            row_param.append(cell_value)

        freight_rule_id = get_freight_rule_id(row_param[1])
        if freight_rule_id != "":
            continue
        else:
            myfile.writelines(gen_rule_sql(default_id, row_param[0], row_param[1], row_param[9]) + '\n')

        # 新疆31、西藏26
        myfile.writelines(gen_rule_prov_sql(default_id, 31, set_map[row_param[2]], amount_map[row_param[2]]) + '\n')
        myfile.writelines(gen_rule_prov_sql(default_id, 26, set_map[row_param[2]], amount_map[row_param[2]]) + '\n')
        # 内蒙古11、青海29、宁夏30、甘肃28
        myfile.writelines(gen_rule_prov_sql(default_id, 11, set_map[row_param[3]], amount_map[row_param[3]]) + '\n')
        myfile.writelines(gen_rule_prov_sql(default_id, 29, set_map[row_param[3]], amount_map[row_param[3]]) + '\n')
        myfile.writelines(gen_rule_prov_sql(default_id, 30, set_map[row_param[3]], amount_map[row_param[3]]) + '\n')
        myfile.writelines(gen_rule_prov_sql(default_id, 28, set_map[row_param[3]], amount_map[row_param[3]]) + '\n')
        # 海南23
        myfile.writelines(gen_rule_prov_sql(default_id, 23, set_map[row_param[4]], amount_map[row_param[4]]) + '\n')
        # 辽宁8
        myfile.writelines(gen_rule_prov_sql(default_id, 8, set_map[row_param[5]], amount_map[row_param[5]]) + '\n')
        # 吉林9
        myfile.writelines(gen_rule_prov_sql(default_id, 9, set_map[row_param[6]], amount_map[row_param[6]]) + '\n')
        # 黑龙江10
        myfile.writelines(gen_rule_prov_sql(default_id, 10, set_map[row_param[7]], amount_map[row_param[7]]) + '\n')

        default_id += 1

    myfile.close()


def read_special_excel(file_path, start_num=1, limit_num=500, default_id=1):
    data = bm.open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[2]
    row_num = (start_num + limit_num) if (start_num + limit_num) < sheets.nrows else sheets.nrows
    for i in range(start_num, row_num):
        row_value = sheets.row_values(i)
        row_param = []
        for j in range(0, sheets.ncols):
            cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
            if j == 0:
                cell_value = cell_value.split("》")[-1]
            elif j == 9:
                if cell_value == "按单加收":
                    cell_value = 2
                else:
                    cell_value = 1

            row_param.append(cell_value)

        freight_rule_id = get_freight_rule_id(row_param[1])
        start_id = default_id
        if freight_rule_id != "":
            start_id = freight_rule_id
        else:
            print(gen_rule_sql(start_id, row_param[0], row_param[1], row_param[9]))

        # 贵州24、云南25
        print(gen_rule_prov_sql(start_id, 24, "1,3", 20))
        print(gen_rule_prov_sql(start_id, 25, "1,3", 20))

        if freight_rule_id == "":
            default_id += 1


def gen_rule_sql(rule_id, rule_name, category_id_ng, rule_type):
    return "INSERT INTO freight_rule(id, rule_name, category_id_ng, type) VALUES ({rule_id},'{rule_name}', {category_id_ng}, {rule_type});".format(
        rule_id=rule_id, rule_name=rule_name, category_id_ng=category_id_ng, rule_type=rule_type)


def gen_rule_prov_sql(freight_rule_id, prov_id, rule_set, freight_amount):
    return "INSERT INTO freight_rule_prov(freight_rule_id, prov_id, rule_set, freight_amount) VALUES({freight_rule_id},{prov_id}, '{rule_set}', {freight_amount});".format(
        freight_rule_id=freight_rule_id, prov_id=prov_id, rule_set=rule_set, freight_amount=freight_amount)


# 获取spuId
def get_freight_rule_id(value_id):
    cur = bm.get_mia_test_cursor("test_admin")
    sql = "SELECT id FROM freight_rule WHERE category_id_ng = " + str(value_id)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return result_data[0][0]
    return ""


# 导出规则
def export_rule_info():
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT " \
          "r.category_id_ng, " \
          "ca.category_name, " \
          "r.rule_name, " \
          "r.type, " \
          "p.prov_id, " \
          "p.rule_set, " \
          "p.freight_amount " \
          "FROM " \
          "(SELECT p4.id AS category_id_ng, CONCAT_WS(' >> ', p1.`name`, p2.`name`, p3.`name`, p4.`name`) AS category_name FROM item_category_ng p1, item_category_ng p2, item_category_ng p3, item_category_ng p4 WHERE p2.parent_id = p1.id AND p3.parent_id = p2.id AND p4.parent_id = p3.id AND p4.is_leaf = 1) ca " \
          "LEFT JOIN freight_rule r ON r.category_id_ng = ca.category_id_ng " \
          "LEFT JOIN freight_rule_prov p ON r.id = p.freight_rule_id limit 300"
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    for data in rows:
        print(data)
    return ""


# 导出模板详情
def export_template_detail(freight_template_id):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT distinct freight_template_id, prov_id,prov_name,rule_type,freight_amount FROM mia_mirror.freight_template_city WHERE freight_template_id = " + str(
        freight_template_id) + " ORDER BY FIELD(`prov_id`, 31, 26, 11, 28,30,29,8,9,10,23,24,25)"
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    xinjiang = next((x for x in rows if x["prov_id"] == 31), None)
    xizang = next((x for x in rows if x["prov_id"] == 26), None)
    neimeng = next((x for x in rows if x["prov_id"] == 11), None)
    gansu = next((x for x in rows if x["prov_id"] == 28), None)
    ningxia = next((x for x in rows if x["prov_id"] == 30), None)
    qinghai = next((x for x in rows if x["prov_id"] == 29), None)

    xinjiang = handel_name(xinjiang)
    xizang = handel_name(xizang)
    neimeng = handel_name(neimeng)
    gansu = handel_name(gansu)
    ningxia = handel_name(ningxia)
    qinghai = handel_name(qinghai)

    sql = "SELECT count(*) AS use_count from item WHERE freight_template_id = " + str(freight_template_id)
    cur.execute(sql)
    use_status = "未使用"
    if cur.fetchall()[0][0] > 0:
        use_status = "已使用"
    print(use_status, xinjiang, xizang, neimeng, gansu, ningxia, qinghai)

    return ""


# 处理名称
def handel_name(xinjiang):
    if xinjiang is not None:
        if xinjiang["rule_type"] == 1:
            xinjiang = "不发"
        elif xinjiang["rule_type"] == 2:
            xinjiang = "包邮"
        elif xinjiang["rule_type"] == 3:
            xinjiang = "加收" + str(int(xinjiang["freight_amount"])) + "元"
    else:
        xinjiang = "包邮"

    return xinjiang


if __name__ == "__main__":
    # 生成规则map
    # duplicate_remove("F:/File/download/分类规则汇总_0321.xlsx", 2, 1, "")
    keynote_amount = {
        '不发/加收30元': 30,
        '不发/加收20元': 20,
        '加收50元': 50,
        '加收20元': 20,
        '包邮发': 0,
        '加收120元': 120,
        '不发/加收40元': 40,
        '加收300元': 300,
        '不发/加收50元': 50,
        '按单加收': 0,
        '不发/加收15元': 15,
        '加收80元发普通快递80,EMS60元顺丰200': 200,
        '加收100元': 100,
        '不发/加收200元': 200,
        '不发/加收130元': 130,
        '不发/加收60元': 60,
        '不发/加收80元': 80,
        '不发/包邮发': 0,
        '按件加收': 0,
        '加收30元': 30,
        '不发/加收10元': 10,
        '不发货': 0,
        '不发货/加收20元': 20,
        '不发': 0,
        '加收10元': 10,
        '不发/加收35元': 35,
        '不发/加收100元': 100
    }

    keynote_set = {
        '不发/加收40元': '1,3',
        '不发/加收10元': '1,3',
        '加收30元': '3',
        '不发货': '1',
        '不发/加收35元': '1,3',
        '不发/加收100元': '1,3',
        '不发/加收130元': '1,3',
        '加收300元': '3',
        '不发/加收50元': '1,3',
        '不发货/加收20元': '1,3',
        '不发/加收200元': '1,3',
        '不发/加收15元': '1,3',
        '不发/加收80元': '1,3',
        '按单加收': '',
        '不发/加收20元': '1,3',
        '不发/包邮发': '1,2',
        '加收100元': '3',
        '加收50元': '3',
        '加收120元': '3',
        '不发': '1',
        '加收20元': '3',
        '按件加收': '',
        '加收10元': '3',
        '包邮发': '2',
        '加收80元发普通快递80,EMS60元顺丰200': '3',
        '不发/加收60元': '1,3',
        '不发/加收30元': '1,3'
    }

    common_amount = {'加收10元': 10, '按单加收': 0, '包邮发': 0}
    common_set = {'加收10元': '3', '按单加收': '', '包邮发': '2'}

    # TRUNCATE test_admin.freight_rule;
    # TRUNCATE test_admin.freight_rule_prov;
    # read_keynote_excel("F:/File/download/分类规则汇总_0321.xlsx", 2, 500, keynote_set, keynote_amount, 1)
    # read_common_excel("F:/File/download/分类规则汇总_0321.xlsx", 2, 2570, common_set, common_amount, 473)
    # read_special_excel("F:/File/download/分类规则汇总_0321.xlsx", 1, 500, 3002)

    # export_rule_info()
    dd = [101]
    for d in dd:
        export_template_detail(d)
