# coding=gbk
import datetime
import pymysql
import json
from pymongo import MongoClient
from collections import OrderedDict
"""
1.mysql数据库导出数据至mongo
2.从mysql查询数据
"""
class ExportData(object):
    mysql_host = None
    mysql_port = None
    mysql_user = None
    mysql_pass = None
    mysql_db = None

    mongo_host = None
    mongo_port = None
    mongo_collection = None

    conn = None
    cursor = None
    mongo = None
    mongodb = None

    def __init__(self,conf_map):
        self.mysql_host = conf_map["mysql_host"]
        self.mysql_port = conf_map["mysql_port"]
        self.mysql_user = conf_map["mysql_user"]
        self.mysql_pass = conf_map["mysql_pass"]
        self.mysql_db = conf_map["mysql_db"]

        self.mongo_host = conf_map["mongo_host"]
        self.mongo_port = conf_map["mongo_port"]
        self.mongo_collection = conf_map["mongo_collection"]

        self.conn = self.get_mysql_conn()
        self.cursor = self.conn.cursor()
        self.mongo = MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.mongodb = self.mongo[self.mongo_collection]

    def get_mysql_conn(self):
        return pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            passwd=self.mysql_pass,
            db=self.mysql_db,
            charset='utf8')

    def set_collection_document(self, table, data):
        if (isinstance(data, dict) == False):
            return False
        else:
            self.mongodb[table].insert(data)

    def show_tables(self):
        self.cursor.execute("show tables")
        data = self.cursor.fetchall()
        return list(map(lambda x : x[0], data))

    def show_actions(self):
        self.cursor.execute("SELECT p.id,p.name,a.id,a.name"
            + " FROM tb_project p"
            + " JOIN tb_module m ON m.project_id = p.id"
            + " JOIN tb_page p2 ON p2.module_id = m.id"
            + " JOIN tb_action_and_page ap ON ap.page_id = p2.id"
            + " JOIN tb_action a ON a.id = ap.action_id")
        data = self.cursor.fetchall()
        return list(map(lambda x : {"projectId":x[0],"projectName":x[1],"actionId":x[2],"actionName":x[3]}, data))

    def show_action(self,actionId):
        actionId = str(actionId)
        self.cursor.execute("SELECT p.id,p.name,a.id,a.name"
                            + " FROM tb_project p"
                            + " JOIN tb_module m ON m.project_id = p.id"
                            + " JOIN tb_page p2 ON p2.module_id = m.id"
                            + " JOIN tb_action_and_page ap ON ap.page_id = p2.id"
                            + " JOIN tb_action a ON a.id = ap.action_id WHERE a.id = " + actionId)
        data = self.cursor.fetchall()
        return list(map(lambda x: {"projectId": x[0], "projectName": x[1], "actionId": x[2], "actionName": x[3]}, data))

    def get_table_desc(self, table):
        sql = """desc %s""" % (table)
        n = self.cursor.execute(sql)
        data = self.cursor.fetchall()
        keys = []
        types = []
        for row in data:
            key = str(row[0])
            if (row[1].find('int') >= 0):
                type = 1
            elif (row[1].find('char') >= 0):
                type = 2
            elif (row[1].find('text') >= 0):
                type = 2
            elif (row[1].find('decimal') >= 0):
                type = 3
            else:
                type = 2
            keys.append(key)
            types.append(type)
        return keys, types

    def drop_collection(self,table):
        self.mongodb[table].drop()

    def export_to_mongo(self, table):
        self.mongodb[table].drop()
        keys, types = self.get_table_desc(table)

        sql = """select * from  %s""" % (table)
        n = self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for row in data:
            ret = {}
            for k, key in enumerate(keys):
                if(types[k] == 1):
                    if row[k]==None:
                        ret[key]= 0
                        continue
                    ret[key] = int(row[k])
                elif(types[k] == 2):
                    if row[k]==None:
                        ret[key]= ''
                        continue
                    ret[key] = str(row[k])
                elif(types[k] == 3):
                    if row[k]==None:
                        ret[key]= ''
                        continue
                    ret[key] = float(row[k])
                else:
                    if row[k]==None:
                        ret[key]= ''
                        continue
                    ret[key] = str(row[k])
            self.set_collection_document(table, ret)

    def __del__(self):
        self.mongo.close()
        self.cursor.close()
        self.conn.close()
"""
1.根据mongo数据生成入参与出参
"""
class GenerateData(object):

    mongo_host = None
    mongo_port = None
    mongo_collection = None
    mongo = None
    mongodb = None

    def __init__(self,conf_map):
        self.mongo_host = conf_map["mongo_host"]
        self.mongo_port = conf_map["mongo_port"]
        self.mongo_collection = conf_map["mongo_collection"]

        self.mongo = MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.mongodb = self.mongo[self.mongo_collection]

    def get_req_param(self,action_id):
        req = self.mongodb["tb_request_parameter_list_mapping"].find({"action_id": action_id},{"parameter_id":1,"_id": 0})
        req_arr = list(map(lambda x: x["parameter_id"], req))
        param = self.mongodb["tb_parameter"].find({"id": {"$in": req_arr}})
        return list(map(lambda x: {"id": x["id"], "name": x["name"], "identifier": x["identifier"], "data_type": x["data_type"]},param))

    def get_res_param(self,action_id):
        res = self.mongodb["tb_response_parameter_list_mapping"].find({"action_id": action_id},{"parameter_id":1,"_id": 0})
        res_arr = list(map(lambda x: x["parameter_id"], res))
        param = self.mongodb["tb_parameter"].find({"id": {"$in": res_arr}})
        return list(map(lambda x: {"id": x["id"], "name": x["name"], "identifier": x["identifier"], "data_type": x["data_type"]},param))

    def get_complex_param(self,complex_parameter_id):
        complex = self.mongodb["tb_complex_parameter_list_mapping"].find({"complex_parameter_id": complex_parameter_id},{"parameter_id":1,"_id": 0})
        complex_arr = list(map(lambda x: x["parameter_id"], complex))
        param = self.mongodb["tb_parameter"].find({"id": {"$in": complex_arr}})
        return list(map(lambda x: {"id": x["id"], "name": x["name"], "identifier": x["identifier"], "data_type": x["data_type"]},param))

    def recursion_param(self,param):
        map={}
        for p in param:
            data_type = p["data_type"]
            identifier = p["identifier"]
            if (not data_type == "object" and not data_type == "array<object>"):
                if("array<" in data_type):
                    map[identifier] = [str(p["name"])]
                else:
                    map[identifier] = p["name"]
            elif (data_type == "object"):
                sub_param = self.get_complex_param(p["id"])
                sub_map = self.recursion_param(sub_param);
                map[identifier] = sub_map
            elif (data_type == "array<object>"):
                sub_param = self.get_complex_param(p["id"])
                sub_map = self.recursion_param(sub_param);
                map[identifier] = [sub_map]
        return map
    # 查询所有的actionId
    def get_all_actionIds(self):
        actions = self.mongodb["my_rap"].find({}, {"actionId": 1, "_id": 0})
        return list(map(lambda x: x["actionId"], actions))

    def find_doc(self,actionId):
        data = self.mongodb["my_rap"].find_one({"actionId": actionId}, {"_id": 0})
        doc = json.dumps(data, sort_keys=True, ensure_ascii=False)
        sorted_doc = json.loads(doc, object_pairs_hook=OrderedDict)
        # self.mongodb["my_rap"].insert(sorted_doc)
        return sorted_doc

    def insert_mongo(self,doc):
        actionId = doc["actionId"]
        doc_str = json.dumps(doc, sort_keys=True, ensure_ascii=False)
        sorted_doc = json.loads(doc_str, object_pairs_hook=OrderedDict)
        self.mongodb["my_rap"].remove({"actionId":actionId})
        self.mongodb["my_rap"].insert(sorted_doc)

# 导数据集成操作
def handle_export_data(tables,ed):
    for table in tables:
        start = datetime.datetime.now()
        ed.export_to_mongo(table)
        print(table + " cost:", (datetime.datetime.now() - start).seconds, "秒")
    print("done")

def handle_generate_data(gd,ed):
    # actions = []
    # if(actionId):
    #     actions = ed.show_action(actionId)
    # else:
    actions = ed.show_actions()
    start = datetime.datetime.now()
    for action_map in actions:
        # print(action_map)
        start1 = datetime.datetime.now()
        try:
            action_id = action_map["actionId"]
            req_list = gd.get_req_param(action_id)
            req_param = gd.recursion_param(req_list)

            res_list = gd.get_res_param(action_id)
            # print(res_list)
            res_param = gd.recursion_param(res_list)

            action_map["requestParam"] = req_param
            action_map["responseParam"] = res_param
            try:
                action_map["serviceId"] = req_param["serviceId"]
            except Exception:
                action_map["serviceId"] = ""
            gd.insert_mongo(action_map)
            print("生成数据",action_id," cost:", (datetime.datetime.now() - start1).seconds, "秒")
        except Exception as e:
            print("操作失败", action_map, e)
    print("生成数据 cost:", (datetime.datetime.now() - start).seconds, "秒")

if __name__ == "__main__":
    conf_map ={
           "mysql_host" :"172.31.10.126",
           "mysql_port" : 3307,
           "mysql_user" : "rap",
           "mysql_pass": "nujsnMk&nrz6cf8umqKr",
           "mysql_db": "rap",
           "mongo_host" : "172.31.10.53",
           "mongo_port" : 27017,
           "mongo_collection":"rap"}

    local_conf_map = {
        "mysql_host": "172.31.10.126",
        "mysql_port": 3307,
        "mysql_user": "rap",
        "mysql_pass": "nujsnMk&nrz6cf8umqKr",
        "mysql_db": "rap",
        "mongo_host": "127.0.0.1",
        "mongo_port": 27017,
        "mongo_collection": "rap"}

    ed = ExportData(conf_map)

    tables = ["tb_parameter",
              "tb_complex_parameter_list_mapping",
              "tb_request_parameter_list_mapping",
              "tb_response_parameter_list_mapping",
              "tb_action",
              "tb_action_and_page",
              "tb_project",
              "tb_module",
              "tb_page"]
    # 导数据过程
    # handle_export_data(tables,ed)

    # 生成数据过程
    gd = GenerateData(conf_map)
    handle_generate_data(gd, ed)
    # handle_generate_data(gd, ed, 469)
