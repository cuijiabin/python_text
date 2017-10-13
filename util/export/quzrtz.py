# coding=utf-8
import sched
import time
from datetime import datetime
import common_build_model as bm
import requests
from multiprocessing import Queue
from collections import deque

queue = deque()
cur = bm.get_mia_cursor()
create_time = datetime.now().strftime("%Y-%m-%d")
# create_time = "2017-08-31"
sql = "SELECT distinct item_id FROM mia_mirror.item_pictures where status = 1 and width = 0 and created_time like '" + create_time + "%'"
with open('e:/pic_size.txt', 'wt') as f:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sql, file=f)
cur.execute(sql)
f_data = cur.fetchall()
# print("本次需要跑出的数组长度 ", len(f_data))
for dd in f_data:
    queue.append(dd[0])

# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def printTime(inc):
    if len(queue) > 0:
        itemId = queue.popleft()
        r = requests.post("http://10.1.51.147:8080/cronTask/itemPicture.htm?itemId=" + str(itemId))
        # print(r.content.decode("utf-8"))
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), itemId)
        schedule.enter(inc, 0, printTime, (inc,))
        # else:
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "完成了")


# 默认参数60s
def checkGen(inc=60):
    schedule.enter(0, 0, printTime, (inc,))
    schedule.run()


# 10s 输出一次
checkGen(0.2)
