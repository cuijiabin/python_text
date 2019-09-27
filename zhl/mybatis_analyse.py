# coding=utf-8
import os
import re
from functools import reduce
from xml.etree.ElementTree import parse

"""
1.首先遍历出xml文件列表 DONE
2.解析mapper文件
"""


# 获取所有的xml文件
def traversing_file(root_dir):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if not os.path.isdir(path) and os.path.splitext(path)[1] == ".xml":
            path = path.replace("\\", "/")
            # if ".java" in path:
            print(path)
            try:
                ana_mapper(path)
                ana_re_mapper(path)
                # count = len(open(path, 'rt').readlines())
                count = len(open(path, 'rb').readlines())
                if count >= 1000:
                    print(path, count)
            except Exception as e:
                print("str(Exception):\t", str(Exception))
                print("str(e):\t\t", str(e))
                print("repr(e):\t", repr(e))
                print("e.message:\t", e.message)

        elif os.path.isdir(path) and ".git" not in path and ".idea" not in path:
            if "src" in path and "test" not in path:
                traversing_file(path)


# 解析mapper文件 ((SELECT.+?FROM)|(LEFT\\s+JOIN|JOIN|LEFT))[\\s`]+?(\\w+)[\\s`]+? TODO select xml 获取内容有一些问题
def ana_mapper(path):
    doc = parse(path)
    tag_list = ["update", "update", "update", "select"]
    for item in doc.iter():
        if item.tag in tag_list:
            # print(item.text)
            u_pattern = re.compile(r"update[\s]+?(\w+)[\s]+?", re.IGNORECASE)
            i_pattern = re.compile(r"update\s+?into[\s]+?(\w+)[\s]+?", re.IGNORECASE)
            d_pattern = re.compile(r"update\s+?from[\s]+?(\w+)[\s]+?", re.IGNORECASE)
            # s_pattern = re.compile(r"select\s+?from[\s]+?(\w+)[\s]+?", re.IGNORECASE)
            s_pattern = re.compile(r"((select.+?from)|(left\s+join|join|left))[\s]+?(\w+)[\s]+?", re.IGNORECASE)
            results = s_pattern.findall(item.text)
            # results.extend(i_pattern.findall(item.text))
            # results.extend(d_pattern.findall(item.text))
            # results.extend(s_pattern.findall(item.text))
            for result in results:
                print(result)


def ana_re_mapper(path):
    with open(path, 'rt', encoding="utf8") as f:
        js_content = reduce(lambda x, y: x + y, f.readlines())
        js_content = js_content.replace('  ', '').replace('\t', '')
        s_pattern = re.compile(r"((select.+?from)|(left\s+join|join|left))[\s]+?(\w+)[\s]+?", re.IGNORECASE)
        results = s_pattern.findall(js_content)
        for result in results:
            print(result[3])


def traversing_java_file(root_dir):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if not os.path.isdir(path) and os.path.splitext(path)[1] == ".java" and "Mapper.java" in path:
            path = path.replace("\\", "/")
            print(path)
            # print(path.split("/")[-1])

        elif os.path.isdir(path) and ".git" not in path and ".idea" not in path:
            if "src" in path and "test" not in path:
                traversing_java_file(path)


if __name__ == "__main__":
    # traversing_java_file("E:/file/project_path/mia_product/mia-framework/mia-store-service")
    # traversing_java_file("E:/file/project_path/mia_product/mia-framework/mia-supplierManager-service")
    all_path = ['mia-common', 'mia-domain', 'mia_log', 'mia-plus-service', 'mia-service', 'mia-store-service',
                'mia-cross-db-query', 'mia-read-service', 'mia-product-service', 'mia-promotion-service',
                'mia-supplierManager-service', 'mia-ums-web', 'mia-order-service', 'mia-store-web',
                'mia-customerservice-task']
    for pp in all_path:
        traversing_java_file("E:/file/project_path/mia_product/mia-framework/" + pp)
