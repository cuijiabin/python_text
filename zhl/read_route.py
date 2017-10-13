# coding=utf-8
import re
import csv

def jiexi():
    f = open('E:/another/zhl/engine/route.js', encoding="utf8")
    s = f.read()
    s = re.sub("//[^\r\n]*", "", s)
    s = s.replace("\n", "")
    pattern = re.compile(r'when(.*, \{.*\})')
    results = pattern.findall(s)

    csv_file = open('E:/route.csv', 'w')
    f_csv = csv.writer(csv_file, dialect='excel')
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

s = jiexi()
i = "wwww"
print("dict[%s]=" % i,s[i] )