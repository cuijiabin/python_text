# coding=utf-8
import sched
import time
from datetime import datetime
import util as bm
import requests
from multiprocessing import Queue
from collections import deque

queue = deque()
f_data = ['http://10.1.51.147:8080/cronTask/reInsureOrder.htm?userId=32997197&orderCode=1907312059033103&parentDstSheetId=64463674',
'http://10.1.51.147:8080/cronTask/reInsureOrder.htm?userId=39819845&orderCode=1907312059298136&parentDstSheetId=64463673',
'http://10.1.51.147:8080/cronTask/reInsureOrder.htm?userId=34318458&orderCode=1908012059452850&parentDstSheetId=64463672',
'http://10.1.51.147:8080/cronTask/reInsureOrder.htm?userId=40674732&orderCode=1908012059477952&parentDstSheetId=64463671',
'http://10.1.51.147:8080/cronTask/reInsureOrder.htm?userId=40253947&orderCode=1908012059639330&parentDstSheetId=64463670',
'http://10.1.51.147:8080/cronTask/reInsureOrder.htm?userId=31216597&orderCode=1908012059732343&parentDstSheetId=64463669',
'http://10.1.51.147:8080/cronTask/reInsureOrder.htm?userId=33729574&orderCode=1908012059785215&parentDstSheetId=64463668']
# print("本次需要跑出的数组长度 ", len(f_data))
for dd in f_data:
    queue.append(dd)

# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def printTime(inc):
    if len(queue) > 0:
        uurl = queue.popleft()
        print(uurl)
        # r = requests.get(uurl)
        # print(r.content.decode("utf-8"))
        schedule.enter(inc, 0, printTime, (inc,))
    else:
        print("完成了")


# 默认参数60s
def checkGen(inc=60):
    schedule.enter(0, 0, printTime, (inc,))
    schedule.run()


# 10s 输出一次
checkGen(1)