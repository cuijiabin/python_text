# coding=utf-8
import random

result = []
for i in range(20):
    num = random.randint(53, 99)
    if num < 10:
        num = "0"+str(num)
    result.append(str(num))
    if i % 10 == 4 or i % 10 == 9:
        print(result)
        result = []
