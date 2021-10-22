#!/usr/bin/python
# coding=utf-8
import os
from ftplib import FTP  # 引入ftp模块


class MyFtp:
    ftp = FTP()

    def __init__(self, host, port=2222):
        self.ftp.connect(host, port)

    def login(self, username, pwd):
        self.ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
        self.ftp.login(username, pwd)
        print(self.ftp.welcome)

    def downloadFile(self, localpath, remotepath, filename):
        os.chdir(localpath)  # 切换工作路径到下载目录
        self.ftp.cwd(remotepath)  # 要登录的ftp目录
        self.ftp.nlst()  # 获取目录下的文件
        file_handle = open(filename, "wb").write  # 以写模式在本地打开文件
        self.ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handle, blocksize=1024)  # 下载ftp文件
        # ftp.delete（filename）  # 删除ftp服务器上的文件

    def close(self):
        self.ftp.set_debuglevel(0)  # 关闭调试
        self.ftp.quit()


# ftp协议文件传输
if __name__ == '__main__':
    ftp = MyFtp('10.5.97.74')
    ftp.login('admin', 'ilbhxuosnfm4736u')
    ftp.downloadFile('E:/file/download/', ' /jobs/results/DES-202004070858-32309900000000/',
                     '323613d7-2993-4df5-a492-759fecc06b35.csv')
    ftp.close()
