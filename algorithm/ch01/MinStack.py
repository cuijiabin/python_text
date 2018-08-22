# coding=utf-8
class NewStack1:
    def __init__(self):
        self.stackData = []
        self.stackMin = []

    def push(self, newNum):
        self.stackData.append(newNum)
        if len(self.stackMin) == 0 or newNum <= self.getMin():
            self.stackMin.append(newNum)

    def pop(self):
        if len(self.stackData) == 0:
            raise Exception("stack is empty!")
        value = self.stackData.pop()
        if self.getMin() == value:
            self.stackMin.pop()
        return value

    def getMin(self):
        if len(self.stackMin) == 0:
            raise Exception("stack is empty!")
        return self.stackMin[-1]


def getAndRemoveLast(stack):
    print("getAndRemoveLast 递归", stack)
    result = stack.pop()
    print("getAndRemoveLast 递归 result", result)
    if len(stack) == 0:
        return result
    else:
        i = getAndRemoveLast(stack)
        stack.append(result)
        print("getAndRemoveLast 递归 append", stack)
        return i


def reverse(stack):
    if len(stack) == 0:
        return
    i = getAndRemoveLast(stack)
    print("getAndRemoveLast", stack)
    reverse(stack)
    print("reverse", stack)
    stack.append(i)
    return stack


# 递归结构有什么妙处？ 稍后准备使用java再实验一次！

def digui(stack):
    print("in", stack)
    if len(stack) == 0:
        return
    m = stack.pop()
    digui(stack)
    stack.append(m)
    print("out", stack)

    return stack


def sort_stack(stack):
    if len(stack) < 2:
        return stack

    help = []
    while stack:
        cur = stack.pop()
        while len(help) != 0 and help[-1] > cur:
            stack.append(help.pop())

        help.append(cur)

    while help:
        stack.append(help.pop())

    return stack

def copy_sort_stack(stack):
    if len(stack) < 2:
        return stack
    help = []

    while stack:
        cur = stack.pop()
        while len(help) > 0 and cur > help[-1]:
            stack.append(help.pop())
        help.append(cur)
    print(help)
    while help:
        stack.append(help.pop())

    return stack

if __name__ == '__main__':
    # stack = NewStack1()
    # stack.push(1)
    # stack.push(2)
    # print(stack.getMin())
    # print(stack.pop())
    # print(stack.pop())

    stack = [1, 2, 3, 9, 5, 6, 7]
    # print(getAndRemoveLast(stack))
    # sort_stack(stack)
    copy_sort_stack(stack)
    while stack:
        print(stack.pop())
    # reverse(stack)
    # for i in range(len(stack)):
    #     print(stack.pop())
