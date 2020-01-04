# coding=utf-8
import json
import time
import os
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
        fout.writelines([head])
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
    import time;
    time.sleep(1)
    print(a + b + c)


if __name__ == '__main__':
    # begin = time.time()
    # splitByLineCount('E:/file/download/tmp_05_1.txt', 10000)
    # end = time.time()
    # print('time is %d seconds ' % (end - begin))

    for i in range(10):
        some(i, i, i)
