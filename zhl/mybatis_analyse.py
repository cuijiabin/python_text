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


def find_java_file(root_dir):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if not os.path.isdir(path):
            search_keys(path)
        elif os.path.isdir(path) and ".git" not in path and ".idea" not in path:
            if "target" not in path and "test" not in path:
                find_java_file(path)


def search_keys(path):
    # print(path)
    file = open(path, 'rb')
    content = file.read()
    file.close()
    content = str(content)
    keys = ['14940', '14346', '14055', '13733', '13680', '13668', '13247', '12919', '15317', '15316', '15315', '15313',
            '15311', '15310', '15308', '15307', '15306', '15305', '15301', '15300', '15299', '15298', '14845', '15175',
            '14664', '12892', '12890', '16481', '16483', '16581', '16582', '16583', '16584', '16585', '16589', '16590',
            '16591', '16587', '16592', '16593', '16594', '16595', '16596', '16597', '16598', '16599', '16600', '16566',
            '16568', '16570', '16572', '16604', '16606', '16615', '16617', '16619', '16622', '16623', '16625', '16631',
            '15898', '16024', '15996', '15997', '15998', '15999', '16000', '16001', '16002', '16003', '16004', '16005',
            '16025', '16018', '16019', '16027', '16020', '16021', '16028', '16634', '16637', '15111', '15050', '15855',
            '15856', '15857', '15858', '15859', '15861', '15862', '15863', '15864', '15865', '15866', '15867', '15868',
            '15869', '15870', '15871', '15872', '15873', '15874', '15875', '15876', '15877', '15878', '15879', '15880',
            '15881', '15882', '15883', '15884', '15885', '15886', '15887', '15888', '15889', '15890', '15891', '15892',
            '15893', '15894', '16351', '15049', '15923', '15924', '15925', '15926', '15927', '15928', '15929', '15930',
            '15931', '15932', '15933', '15934', '15935', '15936', '15937', '15938', '15939', '15940', '14730', '14702',
            '14606', '15899', '15900', '15901', '15902', '15903', '15904', '15905', '15906', '13261', '15921', '15922',
            '15048', '13657', '15907', '15908', '15909', '15910', '15911', '15912', '15913', '15914', '15915', '15916',
            '15917', '15918', '15920', '13047', '15075', '14925', '14924', '13914', '13033', '13031', '13030', '14451',
            '16131', '16139', '16225', '16228', '16253', '16142', '16145', '16147', '16216', '16218', '16220', '16222',
            '16231', '16233', '16235', '16237', '16239', '16242', '16244', '16246', '16248', '16250', '16256', '16258',
            '16260', '16262', '16264', '16266', '15854', '16006', '16007', '16026', '16010', '16011', '16013', '16014',
            '16022', '16029', '16030', '16031']
    for key in keys:
        is_exist = content.find(key)
        if is_exist > 0:
            print(path, key)


if __name__ == "__main__":
    find_java_file("E:/file/project_path/mia_product/order")
    find_java_file("E:/file/project_path/mia_product/order-job")
