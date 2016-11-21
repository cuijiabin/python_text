# coding=gbk
import re
import urllib
import urllib.request
from pyquery import PyQuery as pq
from lxml import etree

def filter_tags(htmlstr):
    # �ȹ���CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # ƥ��CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # ������
    re_h = re.compile('</?\w+[^>]*>')  # HTML��ǩ
    re_comment = re.compile('<!--[^>]*-->')  # HTMLע��
    s = re_cdata.sub('', htmlstr)  # ȥ��CDATA
    s = re_script.sub('', s)  # ȥ��SCRIPT
    s = re_style.sub('', s)  # ȥ��style
    s = re_br.sub('\n', s)  # ��brת��Ϊ����
    s = re_h.sub('', s)  # ȥ��HTML ��ǩ
    s = re_comment.sub('', s)  # ȥ��HTMLע��
    # ȥ������Ŀ���
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replace_char_entity(s)  # �滻ʵ��
    return s


##�滻����HTML�ַ�ʵ��.
# ʹ���������ַ��滻HTML��������ַ�ʵ��.
# ���������µ�ʵ���ַ���CHAR_ENTITIES��,�������HTML�ַ�ʵ��.
# @param htmlstr HTML�ַ���.
def replace_char_entity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entityȫ�ƣ���&gt;
        key = sz.group('name')  # ȥ��&;��entity,��&gt;Ϊgt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # �Կմ�����
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def grap_url(url):
    response = urllib.request.urlopen(url)
    read = response.read()
    read = read.decode("UTF-8")
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
    url = "http://www.ishadowsocks.net/"
    # url = "http://pan.haoii123.com/"
    # grap_url(url)
    v = get_href("http://cndenis.iteye.com/blog/1746706")
    print(v[0])