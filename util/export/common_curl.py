# coding=utf-8
import requests
import json
import hashlib
import datetime
import time

"""
通用网络接口调用工具类

蜜芽圈接口测试
1.口碑接口的api测试
2.定时任务的接口调用
3.其他接口的调用也可以照常试一下

17-05-03 优化出了do_post 下一步需要怎么来处理？
do_get ?
"""


# 输出post结果
def do_post(param):
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(param))
    print(r.content.decode("utf-8"))


# 1.获取口碑列表
def getItemKoubeiList():
    ks_param = {
        "version": "1",
        "class": "Koubei",
        "action": "getKoubeiList",
        "package": "Ums",
        "params": {
            "params": {
                # "id": kId,
                "item_id":1767135,
                # "supplier_id": 566,
                "start_time":"2017 - 07 - 04 00:00:00",
                "end_time":"2017 - 07 - 04 23:00:00",
                "page": 1,
                "limit": 20,
                "status": 2
            }
        }
    }
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(ks_param))
    print(r.content.decode("utf-8"))


# 2.获取口碑评论列表
def getCommentList(sId):
    cl_param = {
        "class": "Comment",
        "action": "getCommentList",
        "package": "ums",
        "params": {
            "params": {
                "subject_id": sId,
                "supplier_id": 1291,  # 还是不管用
                "page": 1,
                "limit": 20,
                "status": 1
            }
        }
    }
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(cl_param))
    print(r.content.decode("utf-8"))


# 3.申诉接口
def supplierKoubeiAppeal(kId):
    ska_param = {
        "class": "Koubei",
        "action": "supplierKoubeiAppeal",
        "params": {
            "supplierId": 1291,
            "koubei_id": kId,
            "koubei_comment_id": 7104,
            "appeal_reason": "申诉原因",
            "supplier_name": "花王旗舰店"
        }
    }
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(ska_param))
    print(r.content.decode("utf-8"))
    # print(json.dumps(ska_param))


# 4.申诉列表
def getKoubeiAppealList():
    ka_param = {
        "class": "Koubei",
        "action": "getKoubeiAppealList",
        "package": "ums",
        "params": {
            "params": {
                "supplier_id": 3054,
                "page": 1,
                "limit": 20
            }
        }
    }
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(ka_param))
    print(r.content.decode("utf-8"))


# 5.对口碑进行回复
def doComemt(sId):
    ka_param = {
        "class": "Comment",
        "action": "comment",
        "params": {
            "subjectId": sId,
            "commentInfo": {
                "comment": "第二条评论",
                "user_id": 7509340,
                "fid": 0
            }
        }
    }
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(ka_param))
    print(r.content.decode("utf-8"))


# 6.商家对口碑进行回复
def doSupplyComemt():
    ka_param = {
        "class": "Koubei",
        "action": "koubeiComment",
        "params": {
            "supplierId": 1291,
            "comment": "供应商的回复2",
            "subjectId": 19646,
            "fid": 0
        }
    }
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(ka_param))
    print(r.content.decode("utf-8"))


# 7.商家对口碑进行回复
def doRank(id):
    ka_param = {
        "class": "Koubei",
        "action": "setKoubeiRank",
        "params": {
            "koubeiIds": id,
            "rank": 1
        }
    }
    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(ka_param))
    print(r.content.decode("utf-8"))


def doSank():
    pp = json.dumps({"content": "测试消息数据内容1",
                     "supplierId": "1291",
                     "subType": 2,
                     "toBeScore": 0,
                     "deductionScore": 12,
                     "canAppeal": 1,
                     "mainType": 1,
                     "appealTime": 3
                     })
    ka_param = {
        "key": "c75da45c44ad9a3e7dfa82a9f6f98d84",
        "function": "push_message",
        "param": pp
    }
    # r = requests.post("http://myums.miyabaobei.com:8089/server_api.htm", data=ka_param)
    r = requests.post("http://erp.pop.miyabaobei.com/server_api.htm", data=ka_param)
    print(r.content.decode("utf-8"))


def md5(s):
    m = hashlib.md5()
    m.update(s.encode(encoding="utf-8"))
    return m.hexdigest()


def doSortPhp():
    # [bill_type = order, source = 5, bill_code = 16021964829384, created_user_id = 10000, message = [缺货](第三方)
    # 该订单商品：4973210993331，联系客户处理；,
    # priority = D, source_remark = 791, label_id = 467, time = 1480648662, token = 292
    # d8e799e6e79ea49c9f508499ce634]
    param = {
        "bill_type": "order",
        "source": "5",
        "label_id": "467",
        "bill_code": "16021964829384",
        "created_user_id": "10000",
        "user_id": "push_message",
        "message": "[缺货](第三方)该订单商品：4973210993331，联系客户处理；",
        "files": "push_message",
        "back_mobile": "push_message",
        "priority": "D",
        "order_item_id": "push_message",
        "relation_user_id": "push_message",
        "source_remark": "791",
        "time": int(time.time())
    }
    # int(time.time())
    start = datetime.datetime.now()
    r = requests.post("http://wangwei_dev.ums.intra.miyabaobei.com/trac/api_trac_issue_pop_sort/index", data=param)
    content = r.content.decode("utf-8")
    print("排序请求cost:", (datetime.datetime.now() - start))

    print(content)
    print(r.headers)

    mdContent = md5(content)
    print(mdContent)
    print(mdContent[:6])
    print(mdContent[26:])
    tokenStr = mdContent[:6] + "mia.com" + mdContent[26:]
    print(tokenStr)
    print(md5(tokenStr))

    param["token"] = md5(tokenStr)

    start = datetime.datetime.now()
    r = requests.post("http://wangwei_dev.ums.intra.miyabaobei.com/trac/api_trac_issue/index", data=param)
    content = r.content.decode("utf-8")
    print("生成工单请求cost:", (datetime.datetime.now() - start))
    print(content)
    print(json.dumps(param))


def doScore():
    pp = {
        "class": "Koubei",
        "action": "getSupplierKoubeiScore",
        "params": {
            "supplier": "3274",
            "search_time": "1487538000"
        }
    }

    # 1487606400 1487692800 1487710800 1487538000

    r = requests.post("http://groupservice.miyabaobei.com/", data=json.dumps(pp))
    print(r.content.decode("utf-8"))


# http://my.ums.intra.miyabaobei.com:8089/server_api.htm

# http://10.1.51.147:8080/cronTask/itemPicture.htm?itemId=1050272

def doresize(itemId):
    r = requests.post("http://10.1.51.147:8080/cronTask/itemPicture.htm?itemId=" + str(itemId))
    print(r.content.decode("utf-8"))


if __name__ == "__main__":
    # getCommentList(19646)
    getItemKoubeiList()
    # getItemKoubeiList(789833)
    # ll = [1753809, 1753810, 1753811, 1718768, 1730065, 1719386, 1719385, 1072259, 1048290, 1048291, 1741022, 1741024, 1753812, 1753813, 1753814, 1753815, 1753816, 1753817, 1753818, 1753819, 1753820, 1753821, 1753822, 1753823, 1753824, 1753825, 1753826, 1753827, 1753828, 1753829, 1753830, 1753831, 1753832, 1753833, 1753836, 1753837]
    # for itemId in ll:
        # doresize(itemId)
        # supplierKoubeiAppeal(27847)
        # getKoubeiAppealList()
        # doComemt(17287)
        # doSank();
        # doSupplyComemt()
        # doRank(27847)
        # doSortPhp()
        # doScore()
