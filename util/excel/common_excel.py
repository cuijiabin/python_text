# coding=utf-8
"""
Excel工具类

功能说明：批量开通口碑服务
"""

import openpyxl
import pandas

import util as bm


# 打开Excel文件
def get_data():
    orderIds = [1, 2, 3]
    items = ['A', 'B', 'C']
    myData = ["风犬少年的天空", "重启", "半泽直树"]
    testData = [orderIds, items, myData]
    return testData


def pd_toexcel(data, file_name):
    """ pandas方式 """
    # 用字典设置DataFrame所需数据 按列添加
    dfData = {
        '序号': data[0],
        '等级': data[1],
        '名称': data[2]
    }
    # 创建DataFrame
    df = pandas.DataFrame(dfData)
    # 存表，去除原始索引列（0,1,2...）
    df.to_excel(file_name, index=False)


def op_toexcel(data, file_name):
    """ openpyxl方式 """
    # 创建工作簿对象
    wb = openpyxl.Workbook()
    # 创建子表
    ws = wb['Sheet']
    # 添加表头
    ws.append(['序号', '等级', '名称'])
    for i in range(len(data[0])):
        d = data[0][i], data[1][i], data[2][i]
        # 每次写入一行
        ws.append(d)
    wb.save(file_name)


# 快团团订单数据导出
def export_ktt_data():
    path = "C:/Users/cuiji/Documents/Devart\dbForge Studio for MySQL/mia主库/快团团-柯扬帆.sql"
    sql = bm.read_sql_file(path)
    # 特殊参数处理
    sql = sql.split(";")[1]
    sql = sql.replace("@begin_time", "'2022-02-01 00:00:00'")
    sql = sql.replace("@end_time", "'2022-02-04 00:00:00'")
    print(sql)
    data_list = bm.get_mia_db_data(sql, "mia")
    df = pandas.DataFrame(data_list)
    df.to_excel('E:/File/download/python_2.xlsx', index=False)


if __name__ == "__main__":
    # export_ktt_data()
    sql_path = "C:/Users/cuiji/Documents/Devart\dbForge Studio for MySQL/mia主库/订单数据修复-考拉订单.sql"
    excel_path = "E:/File/download/python_1.xlsx"
    bm.export_sql_excel(sql_path, excel_path)
