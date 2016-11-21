# coding=gbk
from pymongo import MongoClient
def test_mongo():
    local_client = MongoClient(host="127.0.0.1", port=27017)
    local_db = local_client['rap']

    remote_client = MongoClient(host="172.31.10.53", port=27017)
    remote_db = remote_client['rap']

    cursor = remote_db.my_rap.find()
    for doc in cursor:
        local_db["my_rap"].insert(doc)

test_mongo()