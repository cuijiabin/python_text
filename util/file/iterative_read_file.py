# coding=utf-8
import json
from itertools import islice

'''
迭代文件读取
islice是itertools包里的一个函数
用法为：
iislice(iterable, start, stop,step)
可以返回从迭代器中的start位置，步长为step，直到stop位置的元素。
如果stop为None，则一直迭代到最后位置，step是步长
'''


def iterator_read_file(file_name, num):
    with open(file_name, 'r') as file:
        lice_file = islice(file, num)
        content_list = list(map(lambda x: x.strip('\n'), lice_file))
        while len(content_list) > 0:
            print(json.dumps(content_list))

            lice_file = islice(file, num)
            content_list = list(map(lambda x: x.strip('\n'), lice_file))
    file.close()


if __name__ == '__main__':
    iterator_read_file("E:/File/download/tmp.txt", 20)
