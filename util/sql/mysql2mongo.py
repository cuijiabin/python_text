# coding=utf-8
import multiprocessing
import logging
import time
import pymysql
from pymongo import MongoClient


def test_mongo():
    client = MongoClient(host="127.0.0.1", port=27017)
    db = client['test']
    cursor = db.t_b_action.find()
    for document in cursor:
        print(document)


def test_log():
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    t1 = time.time()
    print(time.time() - t1)
    logger.info("done")


class Mysql2Mongo(object):
    mysql_host = "172.31.10.126"
    mysql_port = 3307
    mysql_user = "rap"
    mysql_pass = "nujsnMk&nrz6cf8umqKr"
    mysql_db = "rap"

    mongo_host = "172.31.10.53"
    mongo_port = 27017

    conn = None
    cursor = None
    mongo = None
    mongodb = None

    def __init__(self, logger):
        self.logger = logger
        self.conn = self.getMysqlConn()
        self.cursor = self.conn.cursor()
        self.mongo = MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.mongodb = self.mongo["rap"]

    def getMysqlConn(self):
        return pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, passwd=self.mysql_pass,
                               db=self.mysql_db, charset='utf8')

    def setMongoCollectionDocument(self, table, data):
        if (isinstance(data, dict) == False):
            return False
        else:
            self.mongodb[table].insert(data)

    def show_tables(self):
        self.cursor.execute("show tables")
        data = self.cursor.fetchall()
        return list(map(lambda x: x[0], data))

    def show_actions(self):
        self.cursor.execute("SELECT p.id,p.name,a.id,a.name"
                            + " FROM tb_project p"
                            + " JOIN tb_module m ON m.project_id = p.id"
                            + " JOIN tb_page p2 ON p2.module_id = m.id"
                            + " JOIN tb_action_and_page ap ON ap.page_id = p2.id"
                            + " JOIN tb_action a ON a.id = ap.action_id")
        data = self.cursor.fetchall()
        return list(map(lambda x: {"projectId": x[0], "projectName": x[1], "actionId": x[2], "actionName": x[3]}, data))

    def show_action(self, actionId):
        self.cursor.execute("SELECT p.id,p.name,a.id,a.name"
                            + " FROM tb_project p"
                            + " JOIN tb_module m ON m.project_id = p.id"
                            + " JOIN tb_page p2 ON p2.module_id = m.id"
                            + " JOIN tb_action_and_page ap ON ap.page_id = p2.id"
                            + " JOIN tb_action a ON a.id = ap.action_id WHERE a.id = " + actionId)
        data = self.cursor.fetchall()
        return list(map(lambda x: {"projectId": x[0], "projectName": x[1], "actionId": x[2], "actionName": x[3]}, data))

    def getMysqlTableDesc(self, table):
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

    def drop_collection(self, table):
        self.mongodb[table].drop()

    def mysql2Mongo(self, table):
        self.mongodb[table].drop()
        keys, types = self.getMysqlTableDesc(table)

        sql = """select * from  %s""" % (table)
        n = self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # print table, keys, types
        for row in data:
            ret = {}
            for k, key in enumerate(keys):
                # if key == 'id':
                #     key = '_id'
                # ret[key] = int(row[k])
                if (types[k] == 1):
                    if row[k] == None:
                        ret[key] = 0
                        continue
                    # print k, key, row
                    ret[key] = int(row[k])
                elif (types[k] == 2):
                    if row[k] == None:
                        ret[key] = ''
                        continue
                    ret[key] = str(row[k])
                elif (types[k] == 3):
                    if row[k] == None:
                        ret[key] = ''
                        continue
                    ret[key] = float(row[k])
                else:
                    if row[k] == None:
                        ret[key] = ''
                        continue
                    ret[key] = str(row[k])
                    # if(table== 'hs_card') or (table== 'hs_hero'):
                    # ret['rand'] = random.random()
            # print(ret)
            self.setMongoCollectionDocument(table, ret)

    def __del__(self):
        self.mongo.close()
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    # test_mongo()
    # test_log()
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    cls = Mysql2Mongo(logger)
    tables = ["tb_parameter", "tb_request_parameter_list_mapping", "tb_response_parameter_list_mapping",
              "tb_complex_parameter_list_mapping", "tb_project", "tb_module", "tb_page", "tb_action_and_page",
              "tb_action"]

    for t in tables:
        t1 = time.time()
        cls.mysql2Mongo(t)
        print(t + " cost:", time.time() - t1)
    logger.info("done")
