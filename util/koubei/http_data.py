# coding=utf-8
"""
Excel工具类

功能说明：批量开通口碑服务
"""
import xdrlib, sys, re, itertools
import xlrd
import requests
import json
import pymysql


# 打开Excel文件
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


def genetate_blank(num):
    if type(num) != int:
        return "参数错误"
    num = 40 - num
    result = " "
    for i in range(num):
        result += " "
    return result


def analyse_excel(file_path):
    # 1.读取Excel
    data = open_excel(file_path)
    # 2.获取一个工作表
    table = data.sheets()[0]
    # 3.获取行数与列数
    row_num = table.nrows
    col_num = table.ncols
    print("这个工作表的行数是：" + str(row_num) + "；行数是：" + str(col_num))
    # 4.输出栏目信息
    columns = table.row_values(0)
    print(columns)
    rule = re.compile(r'[a-zA-z]')

    tables = []
    for i in range(1, row_num):
        row_value = table.row_values(i)
        blank = genetate_blank(len(row_value[8]))
        result = row_value[8] + blank + rule.sub('', row_value[9])
        tables.append(result.lower())

    tables.sort()
    it = itertools.groupby(tables)
    myfile = open('C:/Users/cuijiabin/Desktop/table.txt', 'a')
    myfile.writelines(file_path.split("/")[-1] + '\n')
    myfile.writelines("======================" + '\n')
    for k, g in it:
        myfile.writelines(k + '\n')

    myfile.close()


def getMiaConn():
    conn = pymysql.connect(host="10.1.3.33", user="pop_cuijiabin", passwd="8dtx5EOUZASc", port=3306, charset="utf8")
    return conn


def getAllSeven(supplier_id):
    conn = getMiaConn()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT logo_url FROM db_pop.store_draft where supplier_id  = " + supplier_id)
    data = cur.fetchall()
    if data and len(data) > 0:
        return data[0][0]
    return ""


def analyse_interface(file_path):
    # 1.读取Excel
    data = open_excel(file_path)
    # 2.获取一个工作表
    table = data.sheets()[0]
    # 3.获取行数与列数
    row_num = table.nrows
    col_num = table.ncols
    print("这个工作表的行数是：" + str(row_num) + "；列数是：" + str(col_num))
    # 4.输出栏目信息
    columns = table.row_values(0)
    print(columns)
    for i in range(1, row_num):
        row_value = table.row_values(i)
        supplyId = str(int(row_value[0]))
        supplyName = str((row_value[1]))
        supplyIcon = getAllSeven(str(supplyId))
        # if supplyIcon == "":
        #     print(supplyId, supplyName, "logo为空")

        if supplyName != "" and supplyIcon != "":
            supplyIcon = "http://img.miyabaobei.com/" + supplyIcon
            # print(supplyId,supplyName,supplyIcon)
            # print("INSERT INTO pop_serve_dredge (`supplier_id`, `serve_type`, `is_dredge`) VALUES (%s, 1, 1);" % supplyId)
            # print("curl -d \'{\"class\":\"User\",\"action\":\"addSupplierUser\",\"params\":{\"supplierId\":%s,\"user_info\":{\"nickname\":\"%s\",\"icon\":\"%s\"}}}\' groupservice.miyabaobei.com" % (supplyId,supplyName,supplyIcon))

            payload = {"class": "User",
                       "action": "addSupplierUser",
                       "params": {"supplierId": 7,
                                  "user_info": {"nickname": "戴维贝拉官方旗舰店",
                                                "icon": "http://img.miyabaobei.com/d1/p3/2016/03/24/6c/b4/6cb4c13c7e722ee5c6ebb543acb2bede.png"}
                                  }
                       }
            payload["params"]["supplierId"] = supplyId
            payload["params"]["user_info"]["nickname"] = supplyName
            payload["params"]["user_info"]["icon"] = supplyIcon
            print(json.dumps(payload));
            r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(payload))
            print(r.content.decode("utf-8"))


def getItemSize():

    payload = {
        "urls": "http://img.miyabaobei.com/d1/p1/item/10/1079/1079545_detail_6.jpg, http://img.miyabaobei.com/d1/p1/item/10/1079/1079509_detail_8.jpg"
    }
    r = requests.post("http://img.miyabaobei.com/getimgsize", data=json.dumps(payload))
    print(r.content.decode("utf-8"))


if __name__ == "__main__":

    getItemSize()

    # base = 'E:/File/数据库设计/TableSchema/'
    # list = [base+"001平台数据.xlsx",base+"A01权限管理.xlsx",base+"A02组织管理.xlsx",base+"A03产品管理.xlsx",base+"A04交易体系.xlsx",base+"A05渠道管理.xlsx",base+"A06交易管理.xlsx"]
    # for path in list:
    #     print(path)
    #     analyse_excel(path)

    # analyse_interface("E:/File/download/口碑申报表4.28 更新.xlsx")
    payload = {"class": "User",
               "action": "addSupplierUser",
               "params": {"supplierId": 4966,
                          "user_info": {"nickname": "舒蓓恩专卖店",
                                        "icon": "http://image1.miyabaobei.com/image/2016/11/14/c6d0a5bf6b37ad8dd5e77b3af0297bb5.png"}
                          }
               }
    # payload["params"]["supplierId"] = 4966
    # payload["params"]["user_info"]["nickname"] = "潘明杰"
    # payload["params"]["user_info"]["icon"] = supplyIcon
    print(json.dumps(payload));
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(payload))
    print(r.content.decode("utf-8"))

    # FILEID:d1/p5/2017/07/07/5e/e9/5ee996656bc447fed8e64648bf3d2951228199557.jpg FILEID:d1/p5/2017/07/07/ec/1c/ec1c1934ebc1cf02ccb4ad2b8a355992228627137.jpg


