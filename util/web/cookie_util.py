# coding=gbk
import urllib.request, urllib.parse, urllib.error
import http.cookiejar

"""
              ����      ����
            �����ߩ��������ߩ�
            ��      ?      ��
            ��  �ש�  ����  ��
            ��      ��      ��
            ������      ������
                ��      ����������
                ��  ���ޱ���    �ǩ�
                ��������BUG��   ����
                �����������ש�����
                  ���ϩ�  ���ϩ�
                  ���ߩ�  ���ߩ�
"""
# TODO ʹ��python�������cookie! ��δʵ��
LOGIN_URL = 'http://acm.hit.edu.cn/hoj/system/login'
values = {'user': '******', 'password': '******'} # , 'submit' : 'Login'
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(LOGIN_URL, postdata, headers)
try:
    response = opener.open(request)
    page = response.read().decode()
    # print(page)
except urllib.error.URLError as e:
    print(e.code, ':', e.reason)

cookie.save(ignore_discard=True, ignore_expires=True)  # ����cookie��cookie.txt��
print(cookie)
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)

get_url = 'http://acm.hit.edu.cn/hoj/problem/solution/?problem=1'  # ����cookie���������һ����ַ
get_request = urllib.request.Request(get_url, headers=headers)
get_response = opener.open(get_request)
print(get_response.read().decode())
