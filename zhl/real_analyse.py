# coding=gbk
import re
import csv
from bs4 import BeautifulSoup,Comment,NavigableString,Tag
from functools import reduce

def get_load_view(html_path):
    r_results = []
    try:
        soup = BeautifulSoup(open(html_path, encoding="utf8"), "lxml")
        lvs = soup.find_all("load-view")
        for lv in lvs:
            load_view = lv["src"]
            if("views/module/" not in load_view):
                # print(load_view)
                r_results.append(load_view)
    except Exception:
        print("出错")
    return r_results

def route_analyse():
    rf = open('E:/another/zhl/engine/route.js', encoding="utf8")
    s = rf.read()
    s = re.sub("//[^\r\n]*", "", s)
    s = s.replace("\n", "")
    pattern = re.compile(r'when(.*, \{.*\})')
    results = pattern.findall(s)
    r_results = []
    dict = {};
    for result in results:
        mm = result.split(".when")
        for m in mm:
            m = m.replace(" ", "").replace("+config.version", "").replace("(", "").replace(")", "").replace("{","").replace("}", "")
            if ("resolve:loader" in m):
                r_results.append(m)

    for i in r_results:
        every = i.split(",")
        rou = every[0].replace("'", "")
        view = every[1].replace("templateUrl:'", "").replace("?'", "")
        js = every[3].replace("resolve:loader['", "").replace("'", "").replace("]", "") + ".js"
        js = "engine/controllers/" + js
        dict[view] = rou
        dict[js] = rou
        # print(view)
        lvs = get_load_view("E:/another/zhl/" + view)
        for lv in lvs:
            dict[lv] = rou

    return dict

"""
1.获取所有路由当中涉及到的文件
"""
# dict = route_analyse()
# csv_file = open("E:/route.csv", 'w')
# f_csv = csv.writer(csv_file, dialect='excel')
# f_csv.writerow(["文件名", "路由"])
# for m in dict:
#     print(m,dict[m])
#     f_csv.writerow([m, dict[m]])

def analyse_html(html_path):

    try:
        r_results = []
        soup = BeautifulSoup(open(html_path, encoding="utf8"), "lxml")
        [s.extract() for s in soup("style")]
        [s.extract() for s in soup("script")]
        pattern = re.compile(u"([\u4e00-\u9fff]+)")
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()
        for element in soup(text=lambda text: isinstance(text, NavigableString)):
            if (element.strip() != "" and pattern.findall(element)):
                my = str(element).replace('  ', '').replace('\n', '').replace('\t', '')
                parent = str(element.parent).replace('  ', '').replace('\n', '').replace('\t', '')
                # print("内容：", my)
                # print("父节点：", parent)
                r_results.append(parent)
        r_results = list(set(r_results))
        return r_results
    except Exception:
        print(html_path+"出错")
        return []

"""
2.读取列表内容
"""
# csv_file = open("E:/route0.csv", 'r')
# f_csv = csv.reader(csv_file, dialect='excel')
#
# csv_file_w = open("E:/html.csv", 'w')
# f_csv_w = csv.writer(csv_file_w, dialect='excel')
# f_csv_w.writerow(["文件名", "路由","中文区块"])
#
# for row in f_csv:
#     path = row[0]
#     if(".html" in path):
#         print("html",path)
#         m = analyse_html("E:/another/zhl/"+path)
#         for i in m:
#             try:
#                 print(i)
#                 f_csv_w.writerow([path, row[1], i])
#             except Exception:
#                 print(path + "出错")

def analyse_content(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        pattern = re.compile(u"([\u4e00-\u9fff]+)")
        all_chinese = pattern.findall(content)
        print(content)
        print(reduce(lambda x, y: x + " " + y, all_chinese))

        td_count = len(soup.find_all("td"))
        print("是否td",td_count)
        has_button0 = soup.findAll("button")
        btn_count = len(has_button0)
        print("是否按钮",btn_count)
        return (all_chinese,btn_count)
    except Exception:
        print(content+"出错")
        return ([],0,0)

"""
3.对区块进行分析
"""
csv_file = open("E:/html0.csv", 'r')
f_csv = csv.reader(csv_file, dialect='excel')

csv_file_w = open("E:/effort.csv", 'w')
f_csv_w = csv.writer(csv_file_w, dialect='excel')
f_csv_w.writerow(["文件名", "路由","中文区块","汉字","是否按钮"])

for row in f_csv:
    path = row[0]
    content=row[2]
    effort = analyse_content(content)
    for chinese in effort[0]:
        try:
            f_csv_w.writerow([row[0], row[1], row[2],chinese,effort[1]])
        except Exception:
            print(path + "出错")
# dd = '<div class="fl mt5 ml5">提交订单</div>'
# analyse_content(dd)