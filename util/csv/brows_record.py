# coding=gbk
import csv
import os
from urllib.parse import parse_qs
from urllib.parse import unquote
from urllib.parse import urlparse

from fetch_util import BcnetFetch
from fetch_util import CnblogFetch

"""
浏览记录分析
1.获取所在目录的所有文件
2.读取文件中的url路径
3.选择谷歌url提取关键词

清洗记录 过滤无效url，筛选出谷歌跳转 百度跳转页面！
"""


# 获取所有文件
def get_record_files(base_path="E:/File/浏览记录/08月/"):
    file_names = os.listdir(base_path)
    names = []
    if (len(file_names) > 0):
        for fn in file_names:
            fn = base_path + fn
            names.append(fn)
        return names


# 遍历所有文件
def traversing_file(rootdir="E:/BaiduYunDownload/2015年"):
    names = []
    for parent, _, filenames in os.walk(rootdir):
        for filename in filenames:
            names.append(os.path.join(parent, filename).replace("\\", "/"))
    return names


# 获取单个url列表
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


# 获取所有的url路径
def get_all_urls():
    paths = traversing_file()
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


if __name__ == "__main__":

    traversing_file("E:/File/浏览记录/2017年/")
    urls = get_all_urls()
    print("url数组列表", len(urls))
    h_count = count_host(urls)
    top_10 = sorted(h_count, key=by_score, reverse=True)
    for i in top_10:
        if i[1] <= 10000 and i[1] > 25:
            print(i[0], i[1])

            # bcn = CnblogFetch()
            # for u in filter_url_host(urls, "stackoverflow.com"):
            #     print(u)
            #     bcn.fetch(u)

            # www.google.co.jp 1692
            # github.com 884 GitHub
            # www.zhihu.com 323 知乎
            # www.runoob.com 199 菜鸟教程
            # www.google.com 142
            # twitter.com 127
            # www.xvideos.com 127
            # www.youtube.com 126
            # picture.pconline.com.cn 119 太平洋电脑网

            # zhuanlan.zhihu.com 87 知乎专栏
            # www.pornhub.com 84
            # 36kr.com 84 36氪
            # None 75
            # www.molihua.org 72 茉莉花革命中文网
            # docs.mongodb.com 67 mongodb文档
            # www.freecodecamp.com 66 代码竞赛
            # zh.wikipedia.org 63 维基百科
            # api.crap.cn 56 接口管理系统
            # dev.mysql.com 56 mysql开发文档
            # www.cnblogs.com 55 博客园
            # www.liaoxuefeng.com 54 廖雪峰的网站
            # json.cn 52
            # blog.csdn.net 52 csdn博客频道
            # digi.163.com 51 网易数码测评
            # detail.tmall.com 51 天猫

# 需要进行抓取的网站：www.cnblogs.com blog.csdn.net studygolang.com 知乎 github 然后就没有了！
