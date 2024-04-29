# coding=utf-8
import os
import re

'''
切割文件 按指定行数
提取文件指定字段 行转列
'''


def mk_sub_file(lines, head, filename, sub):
    [des_filename, ext_name] = os.path.splitext(filename)
    filename = des_filename + '_' + str(sub) + ext_name
    print('make file: %s' % filename)
    file_out = open(filename, 'w', encoding='UTF-8')
    try:
        if head is not None and len(head) > 0:
            file_out.writelines([head])
        file_out.writelines(lines)
        return sub + 1
    finally:
        file_out.close()


def split_file_line_count(filename, count, add_header):
    fin = open(filename, 'r', encoding='UTF-8')
    try:
        head = None
        if add_header:
            head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mk_sub_file(buf, head, filename, sub)
                buf = []
        # 最后一个文件处理
        if len(buf) != 0:
            mk_sub_file(buf, head, filename, sub)
    finally:
        fin.close()


# 提取文本字段 并把列转换成行
def extract_file_line_count(filename, count):
    file_in = open(filename, 'r', encoding='UTF-8')
    try:
        buf = []
        sub = 1
        for line in file_in:
            buf.append(line)
            if len(buf) == count:
                sub = extract_sub_file(buf, filename, sub, False)
                buf = []
        # 最后一个文件处理
        if len(buf) != 0:
            extract_sub_file(buf, filename, sub, True)
    finally:
        file_in.close()
        # os.system("start explorer E:\\file\\download")


'''
查了资料，关于open()的mode参数：
‘r’：读
‘w’：写
‘a’：追加
‘r+’ == r+w（可读可写，文件若不存在就报错(IOError)）
‘w+’ == w+r（可读可写，文件若不存在就创建）
‘a+’ ==a+r（可追加可写，文件若不存在就创建）
对应的，如果是二进制文件，就都加一个b就好啦：

‘rb’　　‘wb’　　‘ab’　　‘rb+’　　‘wb+’　　‘ab+’
'''


def extract_sub_file(lines, filename, sub, last):
    [des_filename, ext_name] = os.path.splitext(filename)
    filename = des_filename + '_提取' + ext_name
    file_out = open(filename, 'a+', encoding='UTF-8')
    try:
        content = convert_line(lines)
        if last is False:
            content += ','
        file_out.write(content)
        return sub + 1
    finally:
        file_out.close()


# 行数据转化
def convert_line(lines):
    result_list = []
    for line in lines:
        # split_array = line.split(" ")
        # if len(split_array) < 2:
        #     continue

        # content = split_array[1].replace('  ', '').replace('\n', '')
        content = line.replace('  ', '').replace('\n', '')
        content = "'" + content + "'"
        result_list.append(content)

    return ','.join(result_list)


# 文件批量删除
def remove_file(filename, num):
    for s in range(num):
        file_path = filename + "_" + str(s + 1) + ".txt"
        if os.path.exists(file_path):
            os.remove(file_path)


def split_txt(txt):
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    # pattern = r'\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|。|、|；|‘|’|【|】|·|！| |…|（|）'
    result_list = re.split(pattern, txt)
    for r in result_list:
        print(r)


def read_csv(file_path):
    with open(file_path, encoding="GB2312") as f:
        line = f.readline()
        while line:
            print(line)
            line = f.readline()
        f.close()


if __name__ == '__main__':
    # split_file_line_count('E:/file/download/unlock_order_提取.txt', 200, False)
    # remove_file('E:/file/download/unlock_order', 2)
    split_file_line_count('C:/Users/cuiji/Downloads/部署jar文件/huangcun.sql', 10000, False)
    # read_csv('E:/file/download/8152e680f9978d76400e7a9dcfccfe95.csv')
    # read_csv('E:/file/download/xxx.txt')

    # extract_file_line_count('E:/file/download/line_convert.txt', 100)
