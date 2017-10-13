# coding=utf-8

"""
1.1 旋转字符串
给定一个字符串，要求把字符串前面的若干个字符移动到字符串的尾部，
如把字符串“abcdef”前面的2个字符'a'和'b'移动到字符串的尾部，使得原字符串变成字符串“cdefab”。
请写一个函数完成此功能，要求对长度为n的字符串操作的时间复杂度为 O(n)，空间复杂度为 O(1)。
"""

"""
解法一：暴力移位法

"""
def left_shift_one(s, i, j):
    '''s从i(包含)到j(不包含)，左移一位
    Author: Jasonwbw(Jasonwbw@yahoo.com)
    Editor:
    Args:
        s : 给定需要移位的list
        i : 索引位置i
        j : 索引位置j
    '''
    t = s[i]
    for k in xrange(i, j - 1):
        s[k] = s[k + 1]
    s[j - 1] = t
