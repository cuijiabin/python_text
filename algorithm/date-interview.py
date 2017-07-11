# coding=gbk

"""
日期算法
"""
def isLeapYear(year):
    if (year % 400) == 0:
        return True
    elif (year % 100) != 0 and (year % 4) == 0:
        return True
    else:
        return False


def isLegal(year, month, day):
    if not isinstance(year, int):
        return (False, "year must be numeric")
    if not isinstance(month, int):
        return (False, "month must be numeric")
    if not isinstance(day, int):
        return (False, "day must be numeric")
    if month < 1 or month > 12:
        return (False, "must be between 1 and 12 months")
    if day < 1:
        return (False, "the number of days must be greater than 0")

    return (True, "")


def dayOfYear(year, month, day):
    ok, message = isLegal(year, month, day)
    if not ok:
        print(message)
        return -1

    monthday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if isLeapYear(year):
        monthday[1] = 29

    if day > monthday[month - 1]:
        print("may not exceed the number of days in the month")
        return -1

    result = 0
    for i in range(0, month - 1):
        result += int(monthday[i])
    result += day

    return result


def getLastDay():
    year, month, day = 2017, 2, 4
    result = dayOfYear(year, month, day)
    if result > 0:
        date = str(year) + "-" + str(month) + "-" + str(day)
        print("day of the year %d for date %s is %d" % (year, date, result))


getLastDay()
