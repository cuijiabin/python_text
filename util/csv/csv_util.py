# coding=gbk
import csv
from urllib.parse import unquote
import urllib
from urllib.parse import urlparse

d = {}
with open("E:/File/浏览记录/06月/16-06-12.csv") as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # print(unquote(row[0]))
        # print(row[0],row[1])
        # url = urllib.parse.unquote(row[0])
        url = row[0]
        o = urlparse(url)
        name = o.hostname
        if(name in d):
            arr = d[name]
        else:
            arr = []

        arr.append(url)
        d.setdefault(name, arr)
    for (k,v) in d.items():
        print("地址[%s]=" % k)
        for m in v:
            try:
                print(urllib.parse.unquote(m))
            except Exception:
                print(m)

# if __name__ == "__main__":
#     url = "https://github.com/search?utf8=%E2%9C%93&q=python"
#     # print(unquote(url))
#     print(unquote("%C4%A7%CA%DE"))