# coding=utf-8
import codecs

"""
商家数据中心 各种数据的处理

"""
# 判断是否为数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# 判断是否为整数
def is_int(x):
    try:
        x = int(x)
        return isinstance(x, int)
    except ValueError:
        return False


# 四舍五入 保留两位小数
def round_num(num_str):
    if (is_number(num_str)):
        return str(round(float(num_str), 2))
    return "0"


# 生成sql文件
def handle_file(input_file_name, out_put_file_name, h_f, pre_num):
    out_f = open(out_put_file_name, "a")
    # with open(input_file_name, encoding="utf-8") as in_f:
    with open(input_file_name, encoding="gbk") as in_f:
        cap_count = 0
        size_list = []
        if pre_num > 0:
            for line in in_f.readlines()[0:pre_num]:
                cap_count += 1
                line = line.strip('\n')
                size = line.split("\t")
                size_list.append(size)
                if cap_count >= 10:
                    h_f(size_list, out_f)
                    cap_count = 0
                    size_list = []
        else:
            line = in_f.readline()
            while line:
                cap_count += 1
                line = line.strip('\n')
                size = line.split("\t")
                size_list.append(size)
                if cap_count >= 10:
                    h_f(size_list, out_f)
                    cap_count = 0
                    size_list = []
                line = in_f.readline()

        if len(size_list) > 0:
            h_f(size_list, out_f)

    out_f.close()
    in_f.close()
    print("数据处理完成了")


# 生成活动文件
def gen_prom(size, out_f):
    sql = "INSERT INTO `data_promotion` (supplier_id,promotion_id,deal_num,deal_amount," \
          "order_qty,deal_users,sales_rate) VALUES (" + size[0] + "," + size[1] + "," + size[2] + "," \
          + round_num(size[3]) + "," + size[4] + "," + size[5] + "," + round_num(size[6]) + ");"

    out_f.write(sql)
    out_f.write("\n")


# 生成活动尺码文件
def gen_prom_sku(size, out_f):
    sql = "INSERT INTO `data_promotion_sku` (add_date, supplier_id, promotion_id, " \
          "sku_id, item_size, deal_num, deal_amount, " \
          "order_qty, deal_users, cancel_num, cancel_amount) VALUES ('" \
          + size[0] + "'," + size[1] + "," + size[2] + "," + size[3] + ",'" \
          + size[4] + "'," + size[5] + "," + round_num(size[6]) + "," + size[7] + "," + size[8] + \
          "," + size[9] + "," + round_num(size[10]) + ");"

    out_f.write(sql)
    out_f.write("\n")


# 生成品牌尺码文件
def gen_brand_sku(size, out_f):
    sql = "INSERT INTO `data_brand` (add_date, supplier_id, brand_id, deal_num, deal_amount," \
          "buy_users, promotion_deal_amount,normal_deal_amount) VALUES ('" \
          + size[0] + "'," + size[1] + "," + size[2] + "," + size[3] + "," \
          + round_num(size[4]) + "," + size[5] + "," + round_num(size[6]) + "," + round_num(size[7]) + ");"
    out_f.write(sql)
    out_f.write("\n")
    # print(sql)


"""
线上数据导入
"""


def gen_brand_data(size, out_f):
    sql = "INSERT INTO `data_brand` (add_date, supplier_id, brand_id, deal_num, deal_amount," \
          "buy_users, promotion_deal_amount,normal_deal_amount) VALUES ('" \
          + size[1] + "'," + size[2] + "," + size[3] + "," + size[4] + "," \
          + round_num(size[5]) + "," + size[6] + "," + round_num(size[7]) + "," + round_num(size[8]) + ");"
    out_f.write(sql)
    out_f.write("\n")


def gen_promotion_data(size, out_f):
    sql = "INSERT INTO `data_promotion` (supplier_id,promotion_id,deal_num,deal_amount," \
          "order_qty,deal_users,sales_rate) VALUES (" + size[1] + "," + size[2] + "," + size[3] + "," \
          + round_num(size[4]) + "," + size[5] + "," + size[6] + "," + round_num(size[7]) + ");"
    out_f.write(sql)
    out_f.write("\n")


def gen_promotion_sku_data(size, out_f):
    sql = "INSERT INTO `data_promotion_sku` (add_date, supplier_id, promotion_id, " \
          "sku_id, item_size, deal_num, deal_amount, " \
          "order_qty, deal_users, cancel_num, cancel_amount) VALUES ('" \
          + size[1] + "'," + size[2] + "," + size[3] + "," + size[4] + ",'" \
          + size[5] + "'," + size[6] + "," + round_num(size[7]) + "," + size[8] + "," + size[9] + \
          "," + size[10] + "," + round_num(size[11]) + ");"
    out_f.write(sql)
    out_f.write("\n")


def gen_sku_data(size, out_f):
    sql = "INSERT INTO `data_sku` (add_date, supplier_id, sku_id, deal_num, deal_amount," \
          " buy_users, promotion_deal_amount," \
          "normal_deal_amount, new_user_deal_amount, avg_deal_price, return_rate, cancel_num," \
          "cancel_amount, deal_new_users) VALUES ('" \
          + size[1] + "'," + size[2] + "," + size[3] + "," + size[4] + ",'" + size[5] + "'," \
          + size[6] + "," + size[7] + "," \
          + size[8] + "," + "," + size[9] + "," + size[10] + "," + size[11] + "," + size[12] + "," \
          + size[13] + "," + size[14] + ");"
    out_f.write(sql)
    out_f.write("\n")


def gen_sku_size_data(size, out_f):
    sql = "INSERT INTO `data_sku_size` (add_date, supplier_id, sku_id, item_size, deal_num, " \
          "deal_amount, buy_users, promotion_deal_amount," \
          "normal_deal_amount, return_rate, cancel_num, cancel_amount) VALUES ('" \
          + size[1] + "'," + size[2] + "," + size[3] + "," + size[4] + ",'" + size[5] + "'," \
          + size[6] + "," + size[7] + "," + size[8] + "," \
          + size[9] + "," + size[10] + "," + size[11] + "," + size[12] + ");"
    out_f.write(sql)
    out_f.write("\n")


def gen_supplier_data(list, out_f):
    ml = len(list)
    sql = "INSERT INTO `data_supplier` (add_date, supplier_id, deal_num, deal_amount, order_qty, " \
          "deal_users, deal_new_users, heat, cancel_num, " \
          "cancel_deal_amount, order_cancel_qty, cancel_users) VALUES "
    val = ""
    for idx, size in enumerate(list):
        if idx == (ml - 1):
            val += "('" \
                   + size[0] + "'," + size[1] + "," + size[2] + "," + size[3] + ",'" + size[4] + "'," \
                   + size[5] + "," + size[6] + "," + size[7] + "," + size[8] + "," \
                   + size[9] + "," + size[10] + "," + size[11] + ");"
        else:
            val += "('" \
                   + size[0] + "'," + size[1] + "," + size[2] + "," + size[3] + ",'" + size[4] + "'," \
                   + size[5] + "," + size[6] + "," + size[7] + "," + size[8] + "," \
                   + size[9] + "," + size[10] + "," + size[11] + "),"

    sql += val
    out_f.write(sql)
    out_f.write("\n")


def gen_score_data(list, out_f):
    ml = len(list)
    sql = "INSERT INTO `pop_score_record` (ranking,no_rate,supplier_id," \
          "supplier_name,score_today,num_five," \
          "num_four,num_three,num_two," \
          "num_one,num_default,create_time) VALUES "
    val = ""
    for idx, size in enumerate(list):
        if idx == (ml - 1):
            val += "(" \
                   + size[0] + "," + size[1] + "," + size[2] + ",'" + size[3] + "'," + size[4] + "," \
                   + size[5] + "," + size[6] + "," + size[7] + "," + size[8] + "," \
                   + size[9] + "," + size[10] + ",'" + size[11] + "');"
        else:
            val += "(" \
                   + size[0] + "," + size[1] + "," + size[2] + ",'" + size[3] + "'," + size[4] + "," \
                   + size[5] + "," + size[6] + "," + size[7] + "," + size[8] + "," \
                   + size[9] + "," + size[10] + ",'" + size[11] + "'),"

    sql += val
    out_f.write(sql)
    out_f.write("\n")


if __name__ == "__main__":
    # 批量数据导入不够快
    # handle_file("E:/project_dir/sqlspace/data_brand.txt", "E:/project_dir/sqlspace/data_brand.sql", gen_brand_data, -1)
    # handle_file("E:/project_dir/sqlspace/data_promotion.txt", "E:/project_dir/sqlspace/data_promotion.sql", gen_promotion_data, -1)
    # handle_file("E:/project_dir/sqlspace/data_promotion_sku.txt", "E:/project_dir/sqlspace/data_promotion_sku.sql", gen_promotion_sku_data, -1)
    # handle_file("E:/project_dir/sqlspace/data_sku.txt", "E:/project_dir/sqlspace/data_sku.sql", gen_sku_data, -1)
    # handle_file("E:/project_dir/sqlspace/data_sku_size.txt", "E:/project_dir/sqlspace/data_sku_size.sql", gen_sku_size_data, -1)
    handle_file("E:/project_dir/sqlspace/data_supplier.txt", "E:/project_dir/sqlspace/data_supplier.sql",gen_supplier_data, -1)
    # handle_file("E:/project_dir/sqlspace/score_data.txt", "E:/project_dir/sqlspace/score_data2.sql", gen_score_data, -1)

    # 抽象变量 数据源 数据的判断 数据的分析 数据的输出
    # 采样数据 1.只处理前100行代码
    # for idx, val in enumerate(list):
    #     print(idx, val)
