# coding=utf-8


# 文件对比 查找在b文件中不再在文件中的行内容
def compare_file(file_a, file_b):
    relation = {}
    with open("E:/work-text/" + file_a) as mf:
        line = mf.readline()
        while line:
            line = line.strip('\n')
            relation.setdefault(line, "1")
            line = mf.readline()
        mf.close()

    with open("E:/work-text/" + file_b) as cf:
        line = cf.readline()
        while line:
            line = line.strip('\n')
            if relation.get(line) != "1":
                print(line)

            line = cf.readline()
        cf.close()


if __name__ == '__main__':
    compare_file("tmp_03.txt", "tmp_04.txt")
    compare_file("tmp_04.txt", "tmp_03.txt")
