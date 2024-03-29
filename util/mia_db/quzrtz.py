# coding=utf-8
import sched
import time
from collections import deque

import requests

queue = deque()
url_list = [
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5079079&warehouseId=6715',
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5279948&warehouseId=2655',
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5376323&warehouseId=3364',
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5565212&warehouseId=3364',
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5937773&warehouseId=9769',
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5937770&warehouseId=3364',
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5937770&warehouseId=9769',
    'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5937771&warehouseId=9769'
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
check_gen(0.01)
