# coding=utf-8
import itertools

b = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
for li in itertools.permutations('123456789', 4):
    ret = [i for i in b if i not in li]
    num = int(''.join(li))
    print(num)
    match = True
    for p in li:
        if num % int(p) == 0:
            match = False
            print("内部整除", num, p)
            break

    for q in ret:
        if num % int(q) != 0:
            match = False
            print("外部不整除", num, q)
            break

    if match:
        print("最终结果", num)
