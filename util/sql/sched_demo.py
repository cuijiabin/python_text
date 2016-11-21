# coding=gbk
import time
import sched
from threading import Timer

"""
python定时任务
"""
schedule = sched.scheduler(time.time, time.sleep)


def func(string1, float1):
    print("now is", time.time(), " | output=", string1, float1)


print(time.time())
schedule.enter(2, 0, func, ("test1", time.time()))
schedule.enter(2, 0, func, ("test2", time.time()))
schedule.enter(3, 0, func, ("test3", time.time()))
schedule.enter(4, 0, func, ("test4", time.time()))
schedule.run()
print(time.time())

"""
多线程并发执行
"""
def print_time( enter_time ):
    print("now is", time.time() , "enter_the_box_time is", enter_time)

print(time.time())
Timer(5,  print_time, ( time.time(), )).start()
Timer(10, print_time, ( time.time(), )).start()
print(time.time())