# coding=utf-8
import requests
import time


def read_file(file_path):
    with open(file_path, 'r') as f:
        line = f.readline()
        num = 1
        while line:
            line = line.strip('\n')
            if len(line) == 0:
                continue
            requests.get("http://10.5.108.57:8080/orderTrailInit?thirdOrderCode=" + line)
            if num % 500 == 0:
                print(num, "休眠")
                time.sleep(8)
            num += 1
            line = f.readline()
        f.close()


if __name__ == '__main__':
    read_file('E:/file/download/file.txt')
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # for i in range(3, 34):
    #     file_name = 'E:/file/download/file_' + str(i) + '.txt'
    #     read_file(file_name)
    #     print(file_name)
    #
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
