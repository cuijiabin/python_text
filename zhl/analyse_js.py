# coding=utf-8
import os
import re
import pycorrector
from functools import reduce


def analyse_js(js_path):
    try:
        r_results = []
        with open(js_path, 'rt', encoding="utf8") as f:
            js_content = reduce(lambda x, y: x + y, f.readlines())
            js_content = js_content.replace('  ', '').replace('\t', '')
            note_re = re.compile(u"\/\/[^\n]*")
            content, _ = note_re.subn("", js_content)
            ch_re = re.compile(u"([\u4e00-\u9fff]+)")
            tips = ch_re.findall(content)
            for tip in tips:
                # print(js_path, tip)
                r_results.append(tip)
        r_results = list(set(r_results))
        if len(r_results) > 0 :
            print(js_path, r_results)
        return r_results
    except Exception:
        # print(js_path + "出错")
        return []


# 获取所有的xml文件
def traversing_file(root_dir):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if (not os.path.isdir(path) and os.path.splitext(path)[1] == ".java"):
            path = path.replace("\\", "/")
            analyse_js(path)
        elif (os.path.isdir(path) and ".git" not in path and ".idea" not in path):
            if ("src" in path and "test" not in path):
                traversing_file(path)


"""
1.读取js文件
"""
# analyse_js("F:/project_dir/mywork/mia-framework/mia-store-web/src/main/webapp/WEB-INF/page/all_order/index.jsp")
traversing_file("F:/project_dir/mywork/mia-framework/mia-store-web/src/")

# corrected_sent, detail = pycorrector.correct('少先队员因该为老人让坐')
# print(corrected_sent, detail)
