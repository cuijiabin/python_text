# coding=utf-8
import time
import vthread
from itertools import islice

import requests


def exchagne(a, b):
    print(a, b)
    b, a = a, b
    print(a, b)


def read_file():
    with open("F:/project_dir/origin_data.txt") as of:
        line = of.readline()
        while line:
            line = line.strip('\n')

            line = of.readline()
        of.close()


@vthread.pool(6)
def l_read_file(filename, N):
    with open(filename, 'r') as infile:
        lines_gen = islice(infile, N)
        ids = list(map(lambda x: x.strip('\n'), lines_gen))
        while len(ids) > 0:
            user_ids = ",".join(ids)
            r_data = {
                "userIds": user_ids,
                "write": False
            }
            r = requests.post("http://10.5.107.217:9999/userJob/batchRepairUserLevelInfo", data=r_data)
            print(r.status_code)

            lines_gen = islice(infile, N)
            ids = list(map(lambda x: x.strip('\n'), lines_gen))
    infile.close()


if __name__ == '__main__':
    begin = time.time()
    file_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]
    for s in file_list:
        l_read_file("E:/file/download/tmp/tmp_05_" + s + ".txt", 1000)
    end = time.time()
    print('time is %d seconds ' % (end - begin))
