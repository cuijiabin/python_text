# coding=utf-8


def exchagne(a, b):
    print(a, b)
    b, a = a, b
    print(a, b)


def deppp():
    linNum = 0
    with open("E:/File/download/55.txt", encoding="utf8") as fn:
        linNum = len(list(fn))
        print("文件行数：", linNum)
        fn.close()

    with open("E:/File/download/55.txt", encoding="utf8") as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            if "d1" in line:
                print(line)

            # print(line)
            line = f.readline()
        f.close()


deppp()
