# coding=utf-8

class ListNode():
    def __init__(self, x):
        self.val = x
        self.next = None


def revert(node):
    if node is None or node.next is None:
        return node

    curr = node
    pre = None
    while curr:
        tmp = curr.next
        curr.next = pre
        pre = curr
        if tmp is None:
            break
        curr = tmp

    return curr


if __name__ == "__main__":
    root = ListNode(1)
    p1 = ListNode(2)
    p2 = ListNode(3)
    p3 = ListNode(4)

    root.next = p1
    p1.next = p2
    p2.next = p3

    root = revert(root)
    while root:
        print(root.val)
        root = root.next
