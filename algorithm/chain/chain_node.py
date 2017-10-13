# coding=utf-8

"""
链表反转算法 主要思想循环修改指向

__init__方法在类的一个对象被建立时，马上运行。这个方法可以用来对你的对象做一些你希望的 初始化

"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# 循环的方法反转链表
def nonrecurse(head):
    if head is None or head.next is None:
        return head
    pre = None
    cur = head
    h = head
    while cur:
        h = cur
        tmp = cur.next
        cur.next = pre
        pre = cur
        cur = tmp
    return h


# 递归，head为原链表的头结点，newhead为反转后链表的头结点
def recurse(head, newhead):
    if head is None:
        return
    if head.next is None:
        newhead = head
    else:
        newhead = recurse(head.next, newhead)
        head.next.next = head
        head.next = None
    return newhead


if __name__ == "__main__":
    head = ListNode(1)
    p1 = ListNode(2)
    p2 = ListNode(3)
    p3 = ListNode(4)
    head.next = p1
    p1.next = p2
    p2.next = p3

    head = nonrecurse(head)
    head = recurse(head, None)
    while head:
        print(head.val)
        head = head.next
