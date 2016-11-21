# coding=gbk
import os
import csv
import urllib
from urllib.parse import urlparse
from urllib.parse import unquote
from urllib.parse import parse_qs


def get_record_files(base_path="E:/File/浏览记录/07月/"):
    file_names = os.listdir(base_path)
    names = []
    if (len(file_names) > 0):
        for fn in file_names:
            fn = base_path + fn
            names.append(fn)
        return names


def operate_csv(csv_path):
    urls = []
    try:
        with open(csv_path) as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                url = row[0]
                urls.append(url)
            return urls
    except Exception:
        print("读取文件出错", csv_path)
        return []


# 抓取搜索关键词
def grap_words(urls):
    for url in urls:
        hostname = urlparse(url).hostname
        if (hostname and "www.google" in hostname):
            if ("#" in url):
                u_a = url.split("&q=")
                if (len(u_a) < 2):
                    u_a = url.split("#q=")

                key_word = ""
                if (len(u_a) > 1):
                    try:
                        key_word = unquote(u_a[1])
                        print(key_word)
                    except Exception:
                        print("解析错误", u_a[1], url)


def is_odd(url):
    hostname = urlparse(url).hostname
    return (hostname and "www.google" in hostname and (not "#" in url))


def grap_jump(urls):
    j_urls = []
    for url in list(filter(is_odd, urls)):
        handle = urlparse(url)
        s = parse_qs(handle.query)
        if ("url" in s):
            # print("跳转链接：", s["url"][0])
            j_urls.append(s["url"][0])
    return j_urls


def count_host(urls):
    hostnames = []
    tups = []
    for url in urls:
        hostname = urlparse(url).hostname
        hostnames.append(hostname)

    s = set(hostnames)
    c = [i for i in s]
    for m in c:
        # print(m, hostnames.count(m))
        tups.append((m, hostnames.count(m)))
    return tups


def by_score(t):
    return t[1]


# def get_num():
#     a = [8,2,1,0,3]
#     b = [2,0,3,2,4,0,1,3,2,3,3]
#     tel = ""
#     for i in b:
#         tel += str(a[i])
#     print(tel)

if __name__ == "__main__":

    # get_num()
    path = get_record_files()
    Ls = []
    for p in path:
        # print(p)
        urls = operate_csv(p)
        # 合并数组
        Ls.extend(urls)

    print("url数组列表", len(Ls))
    grap_words(Ls)
    # gls = grap_jump(Ls)
    # L = count_host(gls)
    # all = sorted(L, key=by_score, reverse=True)
    # for i in all:
    #     print(i[0],i[1])
