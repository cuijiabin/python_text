# encoding: utf-8
import os


# 批量查询文件关键信息
def find_java_file(root_dir):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if not os.path.isdir(path):
            search_keys(path)
        elif os.path.isdir(path) and ".git" not in path and ".idea" not in path:
            if "target" not in path and "test" not in path:
                find_java_file(path)


def search_keys(path):
    # print(path)
    file = open(path, 'rb')
    content = file.read()
    file.close()
    content = str(content)
    keys = ['https://m.mia.com', 'https://www.mia.com']
    for key in keys:
        is_exist = content.find(key)
        if is_exist > 0:
            print(path, key)


if __name__ == "__main__":
    find_java_file("E:/file/project_path/mia_product/order")
    find_java_file("E:/file/project_path/mia_product/order-job")
    find_java_file("E:/file/project_path/mia_product/stock")
    find_java_file("E:/file/project_path/mia_product/stock-job")
    find_java_file("E:/file/project_path/mia_product/coupon")
