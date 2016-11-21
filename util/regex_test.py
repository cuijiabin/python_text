# coding=gbk
import re
from bs4 import BeautifulSoup,Comment,NavigableString,Tag

"""
正则测试
1.获取路由表
2.获取load-view
3.使用BeautifulSoup 解析HTML
4.获取所有的html的地址
"""
def testSoup(html_path = "E:/another/zhl/views/order/my/detail_confirmed.html"):
    try:
        soup = BeautifulSoup(open(html_path, encoding="utf8"),"lxml")
        [s.extract() for s in soup("style")]
        [s.extract() for s in soup("script")]
        pattern = re.compile(u"([\u4e00-\u9fff]+)")
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()
        for element in soup(text=lambda text: isinstance(text, NavigableString)):
            if(element.strip()!="" and pattern.findall(element)):
                print("内容：",str(element).replace('  ', '').replace('\n', '').replace('\t', ''))
                print("父节点：",str(element.parent).replace('  ', '').replace('\n', '').replace('\t', ''))
        # for element in soup(text=lambda text: isinstance(text, Tag)):
        #     print("内容：", element)

        # for element in soup():
        #     match = pattern.findall(str(element))
        #     # print("match：", match)
        #     if(not match):
        #         element.extract()
        #     else:
        #         print("内容：",element)


        # print(soup.prettify())
        # print(soup.div.get_text())
        # lvs = soup.find_all("load-view")
        # for lv in lvs:
        #     print(lv["src"])
    except Exception:
        print("出错")

def luyou():
    f = open('E:/another/zhl/engine/route.js', encoding="utf8")
    s = f.read()
    s = re.sub("//[^\r\n]*", "", s)
    s = s.replace("\n", "")
    pattern = re.compile(r'when(.*, \{.*\})')
    results = pattern.findall(s)

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
        print(view,js,rou)
        testSoup("E:/another/zhl/"+view)
    return dict

# luyou()


testSoup("E:/another/zhl/views/order/my/add.html")