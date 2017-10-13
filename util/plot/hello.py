# coding=utf-8
from newspaper import Article
url = "http://blog.csdn.net/jq_ak47/article/details/52685298"
a = Article(url, language='zh') # Chinese
a.download()
a.parse()

print(a.text)
print("=========================title=========================")
print(a.title)
# a.nlp()
# print(a.keywords)