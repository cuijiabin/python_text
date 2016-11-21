# coding=gbk
from nude import Nude

path = "E:/another/git-python/nude.py/examples/images/damita.jpg"

n = Nude(path)
n.parse()
print(n.result, n.inspect())