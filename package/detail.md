问题：如何成为python高手？
函数式编程 性能 测试 编码规范
搜索到的结果都是关于这四个方面的内容的！

====
and
or
not
del
from

while
as
if
else

elif
global

with
assert

pass
yield
break
except
import
print
class
exec
in
raise
continue
finally
is
return
def
for
lambda
try

总共有31个关键字
需要进行一下分组记忆！
import keyword
keyword.kwlist

False
None
True

and
or
not

if
elif
else
pass
break
return
yield  一个带有 yield 的函数就是一个 generator

while
for
continue

try
except
finally
raise


assert
with 紧跟with后面的语句被求值后，返回对象的__enter__()方法被调用，这个方法的返回值将被赋值给as后面的变量。当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法。
in
is
lambda

class
def
del

from
import
as

global 很重要用来定义全局变量
nonlocal

参考：http://blog.csdn.net/longerzone/article/details/17607011

=============================
常见python问题：
1.如何判断字符串为空？
2.乱码问题的常见解决策略？

python 函数参数(必选参数、默认参数、可选参数、关键字参数)

python 输出不换行?

3.python如何返回多个返回值？
采用元组的形式进行返回！return 1, 2, 3

4.python异常的分类？把主要的类型说出来就可以了！

5.python 三木运算 cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]