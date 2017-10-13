# coding=utf-8
import shutil
import os

store_path = "E:/workspace/mia-framework/mia-store-web/logs/store/"
erp_path = "E:/workspace/mia-framework/mia-ums-web/catalina.base_IS_UNDEFINED/logs/ums/"
if os.path.isdir(store_path):
    shutil.rmtree(r"E:/workspace/mia-framework/mia-store-web/logs/store/")
if os.path.isdir(erp_path):
    shutil.rmtree(r"E:/workspace/mia-framework/mia-ums-web/catalina.base_IS_UNDEFINED/logs/ums/")
