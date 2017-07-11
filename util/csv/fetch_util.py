# coding=gbk
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
            "Upgrade-Insecure-Requests": 1,
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
        except Exception:
            print("bcn_fetch出错", url)


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
            read = r.content.decode("utf-8","ignore")
            print("文章抓取：", read)
            soup = BeautifulSoup(read, "lxml")
            title = soup.find('div', class_="zh-question-title").get_text()
            print("文章标题：", title)
            # content = soup.find('div', id="article_content")
            # print("文章内容：", content.get_text())
        except Exception as e:
            print("bcn_fetch出错", url)
            print(format(e))


if __name__ == "__main__":


    # https://www.cnblogs.com/cate/2/
    bnef = CnblogFetch()
    # bnef.fetch("http://www.cnblogs.com/catch/p/6370859.html")
    bnef.fetch("http://ss.ishadow.world/")
