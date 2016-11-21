# coding=gbk
from collections import Iterable
import functools
import gc
import json
from pymongo import MongoClient
from collections import OrderedDict

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('2015-3-25')

# now()

def logger(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@logger('DEBUG')
def today():
    print('2015-3-25')

# today()
# print(today.__name__)
gc.collect()

def test_mongo(document):
    mongo = MongoClient(host="127.0.0.1", port=27017)
    mongodb = mongo["rap"]
    # mongodb["my_rap"].remove({"actionId": id})
    mongodb["my_rap"].insert(document)

def test_find():
    mongo = MongoClient(host="127.0.0.1", port=27017)
    mongodb = mongo["rap"]
    req = mongodb["my_rap"].find({},{"actionId": 1, "_id": 0})
    # print(req)
    # req = self.mongodb["tb_request_parameter_list_mapping"].find({"action_id": action_id},{"parameter_id": 1, "_id": 0})
    req_arr = list(map(lambda x: x["actionId"], req))
    print(req_arr)

def test_find_doc(actionId):
    mongo = MongoClient(host="127.0.0.1", port=27017)
    mongodb = mongo["rap"]
    doc = mongodb["my_rap"].find_one({"actionId":actionId},{"_id": 0})
    print(doc)
    print(type(doc))
    return doc



data = test_find_doc(136)
doc = json.dumps(data,sort_keys=True,ensure_ascii=False)
print(type(doc))
sorted_doc = json.loads(doc,object_pairs_hook=OrderedDict)
print(sorted_doc)
test_mongo(sorted_doc)

# test_find()
# test_find_doc(138)
