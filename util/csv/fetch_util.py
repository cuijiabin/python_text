# coding=utf-8
import io
import sys
import urllib
import requests
from bs4 import BeautifulSoup


# http://pururin.us/ 图片抓取

class BcnetFetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "blog.csdn.net",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }

    def fetch(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            read = r.content.decode("utf-8")
            # print("文章抓取：", read)
            soup = BeautifulSoup(read, "lxml")
            detail = soup.find('div', id="article_details")
            title = detail.find('span', class_="link_title").a.get_text()
            # print("文章标题：", title)
            # content = soup.find('div', id="article_content")
            # print("文章内容：", content.get_text())
        except Exception:
            print("bcn_fetch出错", url)


# 博客园
class CnblogFetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "www.cnblogs.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "upgrade-insecure-requests": '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }

    def fetch(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            read = r.content.decode("utf-8")
            print("文章抓取：", read)
            # soup = BeautifulSoup(read, "lxml")
            # title = soup.find('a', id="cb_post_title_url").get_text()
            # print("文章标题：", title)
            # content = soup.find('div', id="article_content")
            # print("文章内容：", content.get_text())
        except Exception as e:
            print("bcn_fetch出错", url, e)


# 开源中国 抓取之后的编码有问题
class OsChinaFetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "www.oschina.net",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }

    def fetch(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            read = r.content.decode("utf-8")
            print("文章抓取：", read)
            soup = BeautifulSoup(read, "lxml")
            title = soup.find('div', class_="news-content").get_text()
            print("文章标题：", title)
            # content = soup.find('div', id="article_content")
            # print("文章内容：", content.get_text())
        except Exception:
            print("bcn_fetch出错", url)


class SgoFetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "studygolang.com",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }

    def fetch(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            read = r.content.decode("utf-8")
            print("文章抓取：", read)
            soup = BeautifulSoup(read, "lxml")
            title = soup.find('div', class_="title text-center").get_text()
            print("文章标题：", title)
            # content = soup.find('div', id="article_content")
            # print("文章内容：", content.get_text())
        except Exception:
            print("bcn_fetch出错", url)


class ZhiHuFetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "www.zhihu.com",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }

    def fetch(self, url):
        try:
            r = requests.get(url)
            read = r.content.decode("utf-8", "ignore")
            print("文章抓取：", read)
            soup = BeautifulSoup(read, "lxml")
            title = soup.find('div', class_="zh-question-title").get_text()
            print("文章标题：", title)
            # content = soup.find('div', id="article_content")
            # print("文章内容：", content.get_text())
        except Exception as e:
            print("bcn_fetch出错", url)
            print(format(e))


# 文库
class MarxistsFetch(object):
    headers = None

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.marxists.org",
            "Pragma": "no-cache",
            "Referer": "https://www.marxists.org/chinese/maozedong/index.htm",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }

    def fetch(self, url):
        r = requests.get(url, headers=self.headers)
        try:
            read = r.content.decode("gbk", errors='ignore')
        except Exception as e:
            read = r.content.decode("gb18030", errors='ignore')
            print("bcn_fetch出错", url, e)

        soup = BeautifulSoup(read, "html.parser")
        return soup.find('body').get_text()


# 创建一个txt文件，文件名为mytxtfile,并向文件写入msg
def text_create(name, msg):
    # 新创建的txt文件的存放路径
    desktop_path = "E:\\file\\book\\毛泽东选集\\第五卷\\"
    # 也可以创建一个.doc的word文档
    full_path = desktop_path + name + '.txt'
    file = open(full_path, 'w')
    # msg也就是下面的Hello world!
    file.write(msg)
    file.close()


if __name__ == "__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    bnef = MarxistsFetch()
    # bnef.fetch("https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19300105.htm")
    # for i in range(70):
    #     m = i + 1
    #     if m < 10:
    #         m = "0" + str(m)
    #     m = str(m)
    #     print(m)
    #     text_create(m, '')

    print(bnef.fetch('https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19410120.htm'))
    # text_create("05", bnef.fetch("https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19371025.htm"))

    # my_list = []
    # for idx, val in enumerate(my_list):
    #     m = idx + 1
    #     if m < 10:
    #         m = "0" + str(m)
    #     m = str(m)
    #     val = "https://www.marxists.org/chinese/maozedong/" + val
    #     try:
    #         msg = bnef.fetch(val)
    #         text_create(m, msg)
    #     except Exception as e:
    #         text_create(m, val)
    #         print("bcn_fetch出错", m, val, e)
