# coding=utf-8
from itertools import islice

import requests
import vthread


@vthread.pool(3)
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


if __name__ == '__main__':
    # file_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]
    # for s in file_list:
    #     l_read_file("E:/file/download/tmp/tmp_05_" + s + ".txt", 1000)

    # file_list = ["1", "2", "3", "4", "5"]
    # for s in file_list:
    #     # print("E:/file/download/tt/tmp_05_1_1_" + s + ".txt")
    #     l_read_file("E:/file/download/tmp/tmp_05_" + s + ".txt", 500)

    m = []
    n = [44019136]
    for i in m:
        if i not in n:
            print(i)
