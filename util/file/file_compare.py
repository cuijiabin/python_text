# coding=utf-8
from itertools import islice

import requests
import vthread


# @vthread.pool(3)
def l_read_file(filename, N):
    with open(filename, 'r') as infile:
        lines_gen = islice(infile, N)
        ids = list(map(lambda x: x.strip('\n'), lines_gen))
        while len(ids) > 0:
            user_ids = ",".join(ids)
            r_data = {
                "userIds": user_ids,
                "write": True
            }
            r = requests.post("http://10.5.107.217:9999/userJob/batchRepairUserLevelInfo", data=r_data)
            print(r.status_code)

            lines_gen = islice(infile, N)
            ids = list(map(lambda x: x.strip('\n'), lines_gen))
    infile.close()


# 文件对比
def file_check(file_a, file_b):
    relation = {}
    with open("E:/work-text/" + file_a) as mf:
        line = mf.readline()
        while line:
            line = line.strip('\n')
            relation.setdefault(line, "1")
            line = mf.readline()
        mf.close()

    with open("E:/work-text/" + file_b) as genf:
        line = genf.readline()
        while line:
            line = line.strip('\n')
            if relation.get(line) != "1":
                print(line)

            line = genf.readline()
        genf.close()


if __name__ == '__main__':
    file_check("tmp_03.txt", "tmp_04.txt")
    # file_check("pro.txt", "pro-mysql.txt")
    # r_data = {
    #     "logIds": "343883662,343971348,343871316"
    # }
    # r = requests.post("http://10.5.107.217:9999/userJob/batchDelLog", data=r_data)
    # print(r.status_code)
