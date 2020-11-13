# 问题：使用python可以做什么？

    1.网络爬虫
    2.文件处理[excel csv xml 图片处理]
    3.文本处理[读取 写入 切割]
    4.算法实现
    5.定时任务


#### dt = sorted(dt.items(), key=lambda item: item[1], reverse=True)

#### 文件遍历
for parent, _, filenames in os.walk(rootdir):

#### 网络爬虫
util/csv/fetch_util.py

#### csv文件处理
util/csv/brows_record.py

#### 加密算法：
util/date/md5_solve.py

#### 日期转换：
util/date/time_cvt_util.py
#### excel处理：
util/excel/common_excel.py

#### 文件删除：
util/file/delete_util.py
util/file/file_compare.py
util/file/split_file.py

#### 定时任务：
util/mia_db/quzrtz.py

#### 业务相关：
util/mia_db/common_spu.py spu功能查询
util/mia_db/common_stock.py 库存功能查询
util/mia_db/modify_warehouse.py 移仓数据处理
util/mia_db/repair_pre_qty.py 预占库存检查
util/sql/switch_stock_server.py 库存服务模式切换
util/stock_thrift/repair_stock.py 批量库存处理功能