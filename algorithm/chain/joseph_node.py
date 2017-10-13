# coding=utf-8
"""
约瑟夫问题

f[1]=0; 　　f[i]=(f[i-1]+m)%i; (i>1)
"""


def joseph(n, m):
    i, s = 0, 0
    for i in range(2, n - 1):
        s = (s + m) % i
        print(s, i)
    print("the winner is ", s + 1)


if __name__ == "__main__":
    joseph(99, 13)
