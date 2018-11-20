# coding=utf-8
import javalang

f = open('F:/project_dir/mywork/mia-framework/mia-store-web/src/main/java/com/mia/pop/realOrder/mvc/TracInfoController.java',
         encoding="utf8")
s = f.read()
print(s)
tree = javalang.parse.parse(s)
for path, node in tree:
    print(path, node)
