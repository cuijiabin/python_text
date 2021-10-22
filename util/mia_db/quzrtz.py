# coding=utf-8
import sched
import time
from datetime import datetime
import util as bm
import requests
from multiprocessing import Queue
from collections import deque

queue = deque()
url_list = ['http://10.5.105.104:9089/stock/resetStockPreQty?itemId=6047969&warehouseId=3364',
            'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5887008&warehouseId=6868',
            'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=2474565&warehouseId=6868',
            'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5917246&warehouseId=6868',
            'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5960244&warehouseId=6868',
            'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5960245&warehouseId=6868'
            ]
# print("本次需要跑出的数组长度 ", len(url_list))
for url in url_list:
    queue.append(url)

# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def print_time(inc):
    if len(queue) > 0:
        u_url = queue.popleft()
        print(u_url)
        r = requests.get(u_url)
        print(r.content.decode("utf-8"))
        schedule.enter(inc, 0, print_time, (inc,))
    else:
        print("完成了")


# 默认参数60s
def check_gen(inc=60):
    schedule.enter(0, 0, print_time, (inc,))
    schedule.run()


# 10s 输出一次
check_gen(1)
