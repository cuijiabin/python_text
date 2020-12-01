# coding=utf-8
import os
import re
import time

import vthread


def exchagne(a, b):
    print(a, b)
    b, a = a, b
    print(a, b)


def mkSubFile(lines, head, srcName, sub):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('make file: %s' % filename)
    fout = open(filename, 'w')
    try:
        # fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()


def splitByLineCount(filename, count):
    fin = open(filename, 'r')
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf, head, filename, sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf, head, filename, sub)
    finally:
        fin.close()


@vthread.pool(6)
def some(a, b, c):
    time.sleep(1)
    print(a + b + c)


def remove_file(num):
    for s in range(num):
        file_path = "E:/file/download/tt/stock_item_" + str(s + 1) + ".txt"
        if os.path.exists(file_path):
            os.remove(file_path)


def split_txt(txt):
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    # pattern = r'\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|。|、|；|‘|’|【|】|·|！| |…|（|）'
    result_list = re.split(pattern, txt)
    for r in result_list:
        print(r)


if __name__ == '__main__':
    # splitByLineCount('E:/file/download/tt/stock_item.txt', 1000)
    remove_file(85)

    # splitByLineCount('E:/file/download/error/cancel.txt', 2000)
