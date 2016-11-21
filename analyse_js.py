# coding=gbk
import re
import csv
from functools import reduce

def analyse_js(js_path):
    try:
        r_results = []
        with open(js_path, 'rt', encoding="utf8") as f:
            js_content = reduce(lambda x, y: x+y, f.readlines())
            js_content = js_content.replace('  ', '').replace('\t', '')
            note_re = re.compile(u"\/\/[^\n]*")
            content, _ = note_re.subn("", js_content)

            tip_re = re.compile(r"zhlModalTip\s*\((.*?)\)", re.I | re.X)
            tips = tip_re.findall(content)
            func_re = re.compile(u",\s*function\s*\($")
            ch_re = re.compile(u"([\u4e00-\u9fff]+)")
            for tip in tips:
                tip, _ = func_re.subn("", tip)
                ch_tip = ch_re.findall(tip)
                if(len(ch_tip) > 0):
                    # print(tip,"包含中文：",ch_re.findall(tip))
                    r_results.append((tip,ch_re.findall(tip)))
        return r_results
    except Exception:
        print(js_path + "出错")
        return []
"""
1.读取js文件
"""
# analyse_js("E:/another/zhl/"+"engine/controllers/tbdefine/tbjoin_list.js")
csv_file = open("E:/route0.csv", 'r')
f_csv = csv.reader(csv_file, dialect='excel')

csv_file_w = open("E:/js.csv", 'w')
f_csv_w = csv.writer(csv_file_w, dialect='excel')
f_csv_w.writerow(["文件名", "路由","提示信息","中文信息"])

for row in f_csv:
    path = row[0]
    if(".js" in path):
        print("js",path)
        effort = analyse_js("E:/another/zhl/"+path)
        for e in effort:
            # print(e[0],reduce(lambda x, y: x+" "+y, e[1]))
            f_csv_w.writerow([path, row[1], e[0],reduce(lambda x, y: x+" "+y, e[1])])