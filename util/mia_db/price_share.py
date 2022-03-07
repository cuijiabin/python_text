# coding=utf-8
import math


def share_price(price, num):
    # round 表示四舍五入
    avg_price = round(price / num, 2)
    price_list = []
    pre_price = 0
    for i in range(num):
        if i == num - 1:
            last_price = price - pre_price
            price_list.append(last_price)
            continue
        price_list.append(avg_price)
        pre_price += avg_price

    print(price_list)


if __name__ == '__main__':
    share_price(107, 3)
