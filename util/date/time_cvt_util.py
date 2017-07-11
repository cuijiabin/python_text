# coding=gbk
import time

# 日期转换工具
ISFORMAT = "%Y-%m-%d %H:%M:%S"


# 毫秒转化成为年月日
def convert_mill(mill_second):
    print(mill_second, "毫秒转换后", time.strftime(ISFORMAT, time.localtime(mill_second / 1000)))


# 字符串转化成为毫秒
def convert_str_mill(date_str, format="%Y-%m-%d %H:%M:%S"):
    struct_time = time.strptime(date_str, format)
    mk_time = time.mktime(struct_time)
    print(date_str, "转换后毫秒数:" + str(int(1000 * mk_time)))


def convert_str_second(date_str, format="%Y-%m-%d %H:%M:%S"):
    struct_time = time.strptime(date_str, format)
    mk_time = time.mktime(struct_time)
    print(date_str, "转换后毫秒数:" + str(int(mk_time)))


if __name__ == "__main__":
    # convert_mill(1482149183 * 1000)
    # convert_mill(1464278399999)
    convert_str_second("2038-01-01 00:00:00")
    # convert_str_mill("2016-11-14", "%Y-%m-%d")

    print(time.time())
