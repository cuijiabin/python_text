# coding=utf-8
import shutil
import os


def delete_file(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


if __name__ == '__main__':
    file_path_list = ["E:/opt/logs/tt"]
    for file_path in file_path_list:
        delete_file(file_path)
