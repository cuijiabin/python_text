# coding=gbk

def convert(line):
    b_index = line.rfind(" ")
    l_length = len(line)
    v = b_index - l_length
    return line[:v] + "\t" + str(int(line[(v + 1):]) + 18)


def re_name(path="E:/File/download/Ŀ¼.txt"):
    file = open(path)
    while 1:
        line = file.readline()
        if not line:
            break
        print(convert(line))


if __name__ == '__main__':
    re_name()
