# coding=utf-8
import xdrlib, sys, re, itertools
import xlrd
import requests
import json
import pymysql

"""
TODO 貌似没有什么特色的地方
"""

# TODO 一定要转化成为有用的文件


if __name__ == "__main__":


    # with open("F:/File/download/output2.txt", "a+", encoding="utf8") as f:
    #     with open("F:/File/download/tmp.txt", encoding="utf8") as f2:
    #         line = f2.readline()
    #         while line:
    #             newline = "update item set online_time = created_time where id = " + line + ";"
    #             f.writelines(newline + "\n")
    #
    #     f2.close()
    # f.close()

    with open("F:/File/download/tmp.txt", encoding="utf8") as f2:
        line = f2.readline()

        while line:
            line = line.replace("\n", "")
            newline = "update item set online_time = created_time where id = " + line + ";"
            print(newline)

    print("验证完成了")