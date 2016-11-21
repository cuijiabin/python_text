# coding=gbk
"""
查找算法
"""
def binary_search(lst, n):
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = int((low + high) / 2)
        if lst[mid] > n:
            high = mid - 1
        elif lst[mid] < n:
            low = mid + 1
        else:
            return mid
    return -1


if __name__ == '__main__':
    a = [1, 3, 5, 7, 9]
    print(binary_search(a, 3) == 1)
    print(binary_search(a, 4) == -1)
