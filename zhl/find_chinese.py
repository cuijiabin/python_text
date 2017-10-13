# coding=utf-8
import re
import os
import csv

class AnalyseChinese(object):

    csv_file = None
    f_csv = None
    dict = None
    def __init__(self,dict):
        self.dict = dict

    def chushi(self,path):
        self.csv_file = open(path, 'w')
        self.f_csv = csv.writer(self.csv_file, dialect='excel')
        self.f_csv.writerow(["文件名", "行号", "路由", "包含中文", "行内容"])

    def traversing_file(self,rootDir):
        for lists in os.listdir(rootDir):
            path = os.path.join(rootDir, lists)
            if (not os.path.isdir(path)):
                path = path.replace("\\", "/")
                self.analyse_chinese(path)
            if (os.path.isdir(path) and ".git" not in path and ".idea" not in path):
                self.traversing_file(path)

    def analyse_chinese(self,path):
        try:
            with open(path, 'rt', encoding="utf8") as f:
                pattern = re.compile(u"([\u4e00-\u9fff]+)")
                lines = f.readlines()
                rereobj = re.compile(u"\/\/[^\n]*")
                lines, number = reobj.subn("", lines)
                for i in range(len(lines)):
                    results = pattern.findall(lines[i])
                    px = path[15:]
                    route = "无"
                    if(px in self.dict.keys()):
                        route = self.dict[px]
                    if (len(results) > 0):
                        s = ""
                        for result in results:
                            s = s + result + " "
                        self.f_csv.writerow([px,str(i + 1),route,str(s),str(lines[i])])
                f.close()
        except Exception:
            print("读取文件" + path + "出错")

    def save(self):
        self.csv_file.close()

def luyou():
    f = open('E:/another/zhl/engine/route.js', encoding="utf8")
    s = f.read()
    s = re.sub("//[^\r\n]*", "", s)
    s = s.replace("\n", "")
    pattern = re.compile(r'when(.*, \{.*\})')
    results = pattern.findall(s)

    r_results = []

    dict = {};
    for result in results:
        mm = result.split(".when")
        for m in mm:
            m = m.replace(" ", "").replace("+config.version", "").replace("(","").replace(")","").replace("{","").replace("}","")
            if("resolve:loader" in m):
                r_results.append(m)

    for i in r_results:
        every = i.split(",")
        rou = every[0].replace("'", "")
        view = every[1].replace("templateUrl:'", "").replace("?'", "")
        js = every[3].replace("resolve:loader['", "").replace("'", "").replace("]", "") + ".js"
        js = "engine/controllers/" + js
        dict[view] = rou
        dict[js] = rou
    return dict

def test():
    with open("E:/another/zhl/engine/route.js", 'rt', encoding="utf8") as f:
        pattern = re.compile(u"([\u4e00-\u9fff]+)")
        lines = f.readlines()
        print(lines)
        reobj = re.compile(u"\/\/[^\n]*")
        for line in lines:
            line, number = reobj.subn("", line)
            print(line)

if __name__ == '__main__':
    dict = luyou()
    # for i in dict:
    #     print(i,dict[i])

    # m2m = AnalyseChinese(dict)
    # m2m.chushi("E:/engine.csv")
    # m2m.traversing_file("E:/another/zhl/engine")
    # m2m.traversing_file("E:/another/zhl/views")
    # m2m.save()

    test()
    print("ok")