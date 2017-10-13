# coding=utf-8
import re
import urllib
import urllib.request
from pyquery import PyQuery as pq
from lxml import etree

def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replace_char_entity(s)  # 替换实体
    return s


##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replace_char_entity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def grap_url(url):
    response = urllib.request.urlopen(url)
    read = response.read()
    read = read.decode("ISO-8859-1")
    read = filter_tags(read)
    print(read)

def get_href(url):
    response = urllib.request.urlopen(url)
    read = response.read()
    read = read.decode("UTF-8")
    return re.findall('<a.*?href=.*?<\/a>',read,re.I)

def get_img(url):
    response = urllib.request.urlopen(url)
    read = response.read()
    read = read.decode("UTF-8")
    return re.findall('<img.*?src=.*?>',read,re.I)

if __name__ == '__main__':
    # url = "https://detail.tmall.hk/hk/item.htm?spm=a1z10.4-b-s.w5003-15745601448.3.cTLysz&id=540000229842&rn=71a39db269e8a9227c205e1c0f41d495&abbucket=4&scene=taobao_shop&skuId=3201014554263"
    url = "http://ss.ishadow.world/"
    grap_url(url)
    # v = grap_url("http://cndenis.iteye.com/blog/1746706")
    # print(v[0]) encoding = "ISO-8859-1"