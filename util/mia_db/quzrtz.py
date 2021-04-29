# coding=utf-8
import sched
import time
from datetime import datetime
import util as bm
import requests
from multiprocessing import Queue
from collections import deque

queue = deque()
f_data = ['http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5917249&warehouseId=6868',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5917243&warehouseId=6868',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5917242&warehouseId=6868',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5917241&warehouseId=6868',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5917250&warehouseId=6868',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5917239&warehouseId=6868']
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
        r = requests.get(uurl)
        print(r.content.decode("utf-8"))
        schedule.enter(inc, 0, printTime, (inc,))
    else:
        print("完成了")


# 默认参数60s
def checkGen(inc=60):
    schedule.enter(0, 0, printTime, (inc,))
    schedule.run()


# 10s 输出一次
checkGen(1)
