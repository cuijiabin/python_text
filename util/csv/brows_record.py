# coding=utf-8
import csv
import os
from urllib.parse import parse_qs
from urllib.parse import unquote
from urllib.parse import urlparse

# from fetch_util import BcnetFetch
# from fetch_util import CnblogFetch
#
# from newspaper import Article

"""
浏览记录分析
1.获取所在目录的所有文件
2.读取文件中的url路径
3.选择谷歌url提取关键词

清洗记录 过滤无效url，筛选出谷歌跳转 百度跳转页面！
"""


# 获取所有文件
def get_record_files(base_path="E:/File/浏览记录/09月/"):
    file_names = os.listdir(base_path)
    names = []
    if (len(file_names) > 0):
        for fn in file_names:
            fn = base_path + fn
            names.append(fn)
        return names


# 遍历所有文件
def traversing_file(rootdir="E:/File/浏览记录/2018年/"):
    names = []
    for parent, _, filenames in os.walk(rootdir):
        for filename in filenames:
            names.append(os.path.join(parent, filename).replace("\\", "/"))
    return names


# 获取单个url列表
def operate_csv(csv_path):
    urls = []
    try:
        with open(csv_path, encoding="utf8") as f:
            # f_csv = csv.reader(f)
            line = f.readline()
            while line:
            # for row in f_csv:
                url = line[0]
                urls.append(url)
            return urls
    except Exception as e:
        print("读取文件出错", csv_path, e)
        return []


# 获取所有的url路径
def get_all_urls(root):
    paths = traversing_file(root)
    all_urls = []
    for path in paths:
        urls = operate_csv(path)
        all_urls.extend(urls)
    return all_urls


# 抓取搜索关键词
def get_grap_words(urls):
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


# 判断是否为跳转url
def is_jump(url):
    hostname = urlparse(url).hostname
    return (hostname and "www.google" in hostname and (not "#" in url))


# 获取谷歌的跳转链接
def get_jump_url(urls):
    j_urls = []
    for url in list(filter(is_jump, urls)):
        handle = urlparse(url)
        qs = parse_qs(handle.query)
        if ("url" in qs):
            j_urls.append(qs["url"][0])
    return j_urls


# 按host来计数
def count_host(urls):
    hostnames = []
    tups = []
    for url in urls:
        hostname = urlparse(url).hostname
        hostnames.append(hostname)

    s = set(hostnames)
    c = [i for i in s]
    for m in c:
        tups.append((m, hostnames.count(m)))
    return tups


# 排序函数
def by_score(t):
    return t[1]


# 按host进行过滤
def filter_url_host(urls, hostname):
    retults = []
    for url in urls:
        u_host = urlparse(url).hostname
        if u_host == hostname:
            retults.append(url)

    retults = set(retults)
    return retults


# def analyse_title(address):
#     try:
#         a = Article(address, language='zh')  # Chinese
#         a.download()
#         a.parse()
#         # print(a.text)
#         # print("=========================title=========================")
#         print(a.title)
#     except Exception:
#         print("抓取失败")

if __name__ == "__main__":

    # 获取目录下所有的url
    urls = get_all_urls("F:/File/浏览记录/2018年/08月")
    # 分析url的关键搜索词
    # get_grap_words(urls)

    # 常用访问网站前十名
    print("url数组列表", len(urls))
    # for url in urls:
    #     if "stackoverflow.com" in url:
    #         print(url)
    #         analyse_title(url)

    for u in filter_url_host(urls, "github.com"):
        print(u)

    # h_count = count_host(urls)
    # top_10 = sorted(h_count, key=by_score, reverse=True)
    # for i in top_10:
    #     if i[1] <= 10000 and i[1] > 25:
    #         print(i[0], i[1])

            # bcn = CnblogFetch()
            #     bcn.fetch(u)

            # github.com
            # www.zhihu.com
            # www.google.com
            # blog.csdn.net
            # www.jianshu.com
            # www.oschina.net
            # stackoverflow.com
            # translate.google.cn
            # news.dwnews.com
            # www.cnblogs.com
            # zh.wikipedia.org
            # git.oschina.net
            # kr.com
            # zhuanlan.zhihu.com

# 需要进行抓取的网站：www.cnblogs.com blog.csdn.net studygolang.com 知乎 github 然后就没有了！
