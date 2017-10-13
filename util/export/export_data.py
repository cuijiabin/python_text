# coding=utf-8
import pymysql

import json
import csv
import re

"""
问题：excel 时间格式 一次性批量导出数据！
此文件为 build_model common_excel common_export 文件的组合 专门用于处理数据导出问题
"""

# TODO 根据合同号 品牌id 获取扣点
"""
"select kd_rate from mia_mirror.contract_brand_kd_rate_cycle "
"where contract_no = %s "
"and brand_id = " + str(brandId) + " and status = 1 "
"and NOW() BETWEEN start_date and end_date
"""
# TODO 根据供应商id 品牌id 获取品牌资质类信息
"""
"select qualification_type,is_has,expiration_time from vr_pop.pop_supplier_brand_qualification where supplier_id = " + str(
supplierId) + " and brand_id = " + str(brandId))
"""


def getStatus(type, status):
    try:
        zhmap = {
            1: "有效",
            2: "未审核",
            -1: "作废",
            -2: "冻结",
            -3: "不合作"
        }
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
        zjmap = {
            1: '有',
            2: '无'
        }
        if not status:
            return ""
        if type == 1:
            return zhmap[status]
        if type == 2:
            return htmap[status]
        if type == 3:
            return zjmap[status]
    except Exception as e:
        print("map错误", type, status)
    return ""


def convert():
    csv_file_w = open("E:/005.csv", 'w')
    f_csv_w = csv.writer(csv_file_w, dialect='excel')
    # 所有供应商id
    all = getAllSeven()
    for supplierId in all:
        # 获取供应商详情
        allsupplier = getSupplierInfo(supplierId)
        for supplier in allsupplier:
            contractInfo = getContractNo(supplier[0])
            contractNo = contractInfo[0]
            # 合同状态
            contractStatus = contractInfo[1]
            # zhuying = getCategoryInfo(supplier[3])
            fzr = getSecUserName(supplier[4])
            allbrandinfo = getBrandInfo(supplier[0])
            partnerStatus = getPartnerLogin(supplier[1])
            for brand in allbrandinfo:
                ppmc = getBrandName(brand[0])
                qqq = getQualification(supplier[0], brand[0])
                # zylm = getCategoryInfo(brand[1])
                # kd = getKdRate(contractNo, brand[0])
                # print(supplier[1],supplier[2],zhuying,brand[0],ppmc,zylm,supplier[4],fzr,kd)
                try:
                    # print(supplier[1], supplier[2], partnerStatus,getStatus(1,partnerStatus), contractNo, getStatus(2,contractStatus), fzr, brand[0], ppmc,
                    #       qqq[0], getStatus(3,qqq[1]), qqq[2])
                    f_csv_w.writerow([supplier[1], supplier[2], getStatus(1, partnerStatus), contractNo,
                                      getStatus(2, contractStatus), fzr, brand[0], ppmc,
                                      qqq[0], getStatus(3, qqq[1]), qqq[2]])
                except UnicodeEncodeError as ue:
                    print("读取文件" + str(brand[0]) + "出错" + str(supplier[1]) + "字符串问题")
                except Exception as e:
                    print("读取文件" + str(brand[0]) + "出错" + str(supplier[1]))


def writeResult():
    csv_file_w = open("E:/effort.csv", 'w')
    f_csv_w = csv.writer(csv_file_w, dialect='excel')
    f_csv_w.writerow(["文件名", "路由", "中文区块", "汉字", "是否按钮"])


# 获取单个url列表
def read_csv(csv_path="E:/all.csv"):
    # csv_file_w = open("E:/006.csv", 'w')
    # f_csv_w = csv.writer(csv_file_w, dialect='excel')
    mmap = {
        "1": "待部门审核",
        "2": "待财务审核",
        "3": "待法务审核",
        "4": "待CEO审核",
        "5": "审核成功",
        "6": "撤销",
        "7": "驳回",
        "8": "作废"
    }
    smap = {
        "-1": "作废",
        "1": "正常"
    }
    try:
        with open(csv_path) as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                supplierName = getSupplierName(row[0])
                supplier = getSupplierInfo(row[0])
                fzr = getSecUserDeptName((supplier[4]))
                userName = getSecUserDeptName(row[1])
                brandName = getBrandName(row[3])
                stat1 = ""
                stat2 = ""
                try:
                    stat1 = smap[row[8]]
                    stat2 = mmap[row[9]]
                except Exception:
                    print("状态出错", row[9])

                # f_csv_w.writerow(supplierName, str(row[0]), userName[1], userName[0], row[2], brandName, row[4], row[5],
                #                  str(row[6]), str(row[7]), stat2, stat1)
                wordList = [supplier[2], row[0], userName[1], userName[0], row[1], brandName, row[4],
                            row[5], row[6], row[7], stat2, stat1, fzr[0], fzr[1]]
                print('==='.join(wordList))
    except Exception:
        print("读取文件出错", csv_path)

    f.close()


if __name__ == "__main__":
    # 供应商id  mia_supplier_id vr_pop.pop_customer_supplier
    # 供应商名称 name vr_pop.pop_customer_supplier
    # 供应商账号状态 status mia_mirror.partner_login 1有效 2 未审核  -1作废 -2冻结 TODO
    # 合同id contract_no vr_pop.procurement_contract
    # 合同状态 status vr_pop.procurement_contract 枚举值？
    # 招商负责人 supplier_admin_id vr_pop.pop_customer_supplier
    # 品牌id  brand_id vr_pop.pop_supplier_brand
    # 品牌名称 name item_brand
    # 证件名称 qualification_type vr_pop.pop_supplier_brand_qualification TODO
    # 证件状态 is_has vr_pop.pop_supplier_brand_qualification 1 - '有' 2 - '无' TODO
    # 有效期时间 expiration_time vr_pop.pop_supplier_brand_qualification TODO

    # read_csv()


    # for i in ll:
    #     if i in kt:
    #         print("开通")
    #     else:
    #         print("未开通")
