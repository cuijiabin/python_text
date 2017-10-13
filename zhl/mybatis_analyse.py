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
        if (not os.path.isdir(path) and os.path.splitext(path)[1] == ".java"):
            path = path.replace("\\", "/")
            # if (".java" in path):
                # print(path)
            try:
                # ana_mapper(path)
                # ana_re_mapper(path)
                count = len(open(path, 'rt').readlines())
                if(count >= 1000):
                    print(path,count)
            except Exception as e:
                print("str(Exception):\t", str(Exception))
                print("str(e):\t\t", str(e))
                print("repr(e):\t", repr(e))
                print("e.message:\t", e.message)
                print("traceback.print_exc():\t", traceback.print_exc())
                print("traceback.format_exc():\n%s" % traceback.format_exc())

        elif (os.path.isdir(path) and ".git" not in path and ".idea" not in path):
            if ("src" in path and "test" not in path):
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

if __name__ == "__main__":
    all_path = ["mia-common", "mia-customerservice-task", "mia-data-service", "mia-data-web", "mia-domain",
                "mia-order-service", "mia-popscore-service", "mia-product-service", "mia-promotion-service",
                "mia-read-service", "mia-service", "mia-store-service", "mia-store-web", "mia-supplierManager-service",
                "mia-ums-service", "mia-ums-web", "mia_log"]
    for pp in all_path:
        traversing_file("E:/workspace/mia-framework-new/" + pp)

    # E:/workspace/mia-framework-new/mia-product-service/src/main/java/com/mia/pop/ums/product/main/dao/ProcurementOrderDetailMapper.xml 有问题的
    # ana_re_mapper(
    #     "E:/project_dir/javaspace/mia-framework-oneall/mia-service/src/main/java/com/mia/common/api/dao/CommunityTodoMapper.xml")
