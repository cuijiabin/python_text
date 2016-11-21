# coding=gbk
import re
import os
import codecs
import logging
import xlwt
import xlrd
import csv
from functools import reduce

# logging.basicConfig(filename='E:/代码中文结果.txt',level=logging.DEBUG)


"""
删除空格
"""
def delblankline(infile, outfile):
    """ Delete blanklines of infile """
    infp = open(infile, "r")
    outfp = open(outfile, "w")
    lines = infp.readlines()
    for li in lines:
        if li.split():
            outfp.writelines(li)
    infp.close()
    outfp.close()

"""
合并多个文件
"""
def delblanklinelist(infile, outfile):
    """ Delete blanklines of infile """

    outfp = open(outfile, "w")
    for inf in infile:
        infp = open(inf, "r")
        lines = infp.readlines()
        for li in lines:
            if li.split():
                outfp.writelines(li)
        infp.close()
    outfp.close()

"""
去重
"""
def remove_deduplication(infile, outfile):
    arr = []
    infp = open(infile, "r")
    outfp = open(outfile, "w")
    lines = infp.readlines()
    for li in lines:
        if li.split() and li.split(",")[3] not in arr:
        # if li.split():
            outfp.writelines(li)
            # print(li.split(",")[3])
            arr.append(li.split(",")[3])
            # arr = list(set(arr))
    infp.close()
    outfp.close()


if __name__ == '__main__':

    # delblankline("E:/js.csv","E:/js0.csv")
    remove_deduplication("E:/html.csv", "E:/html3.csv")
    print("ok")