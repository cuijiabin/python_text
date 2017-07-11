# coding=gbk
import csv
import os
from urllib.parse import parse_qs
from urllib.parse import unquote
from urllib.parse import urlparse

from fetch_util import BcnetFetch
from fetch_util import CnblogFetch

"""
�����¼����
1.��ȡ����Ŀ¼�������ļ�
2.��ȡ�ļ��е�url·��
3.ѡ��ȸ�url��ȡ�ؼ���

��ϴ��¼ ������Чurl��ɸѡ���ȸ���ת �ٶ���תҳ�棡
"""


# ��ȡ�����ļ�
def get_record_files(base_path="E:/File/�����¼/08��/"):
    file_names = os.listdir(base_path)
    names = []
    if (len(file_names) > 0):
        for fn in file_names:
            fn = base_path + fn
            names.append(fn)
        return names


# ���������ļ�
def traversing_file(rootdir="E:/BaiduYunDownload/2015��"):
    names = []
    for parent, _, filenames in os.walk(rootdir):
        for filename in filenames:
            names.append(os.path.join(parent, filename).replace("\\", "/"))
    return names


# ��ȡ����url�б�
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
        print("��ȡ�ļ�����", csv_path)
        return []


# ��ȡ���е�url·��
def get_all_urls():
    paths = traversing_file()
    all_urls = []
    for path in paths:
        urls = operate_csv(path)
        all_urls.extend(urls)
    return all_urls


# ץȡ�����ؼ���
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
                        print("��������", u_a[1], url)


# �ж��Ƿ�Ϊ��תurl
def is_jump(url):
    hostname = urlparse(url).hostname
    return (hostname and "www.google" in hostname and (not "#" in url))


# ��ȡ�ȸ����ת����
def get_jump_url(urls):
    j_urls = []
    for url in list(filter(is_jump, urls)):
        handle = urlparse(url)
        qs = parse_qs(handle.query)
        if ("url" in qs):
            j_urls.append(qs["url"][0])
    return j_urls


# ��host������
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


# ������
def by_score(t):
    return t[1]


# ��host���й���
def filter_url_host(urls, hostname):
    retults = []
    for url in urls:
        u_host = urlparse(url).hostname
        if u_host == hostname:
            retults.append(url)

    retults = set(retults)
    return retults


if __name__ == "__main__":

    traversing_file("E:/File/�����¼/2017��/")
    urls = get_all_urls()
    print("url�����б�", len(urls))
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
            # www.zhihu.com 323 ֪��
            # www.runoob.com 199 ����̳�
            # www.google.com 142
            # twitter.com 127
            # www.xvideos.com 127
            # www.youtube.com 126
            # picture.pconline.com.cn 119 ̫ƽ�������

            # zhuanlan.zhihu.com 87 ֪��ר��
            # www.pornhub.com 84
            # 36kr.com 84 36�
            # None 75
            # www.molihua.org 72 ���򻨸���������
            # docs.mongodb.com 67 mongodb�ĵ�
            # www.freecodecamp.com 66 ���뾺��
            # zh.wikipedia.org 63 ά���ٿ�
            # api.crap.cn 56 �ӿڹ���ϵͳ
            # dev.mysql.com 56 mysql�����ĵ�
            # www.cnblogs.com 55 ����԰
            # www.liaoxuefeng.com 54 ��ѩ�����վ
            # json.cn 52
            # blog.csdn.net 52 csdn����Ƶ��
            # digi.163.com 51 �����������
            # detail.tmall.com 51 ��è

# ��Ҫ����ץȡ����վ��www.cnblogs.com blog.csdn.net studygolang.com ֪�� github Ȼ���û���ˣ�
