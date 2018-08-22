# coding=utf-8
"""
产品与招商负责人关系表 对应关系的检查工具!哈哈哈

"""


# 关联合并数据 用来检查招商负责人与产品的关系！
def merge_file():
    # 1.获取用户关系映射
    relation = {}
    with open("F:/project_dir/relation.txt") as rf:
        line = rf.readline()
        while line:
            line = line.strip('\n')
            size = line.split("\t")
            relation.setdefault(size[0], size[1])
            line = rf.readline()
        rf.close()
    # 2.读取原生数据
    merfile=open("F:/project_dir/merge.txt","a")
    with open("F:/project_dir/origin_data.txt") as of:
        line = of.readline()
        while line:
            line = line.strip('\n')
            size = line.split("\t")
            if relation.get(size[1]):
                new_str = size[0] +"\t"+relation[size[1]]+"\t"+size[2]
                merfile.write(new_str)
                merfile.write('\n')

            line = of.readline()
        of.close()
        merfile.close()


# 文件对比
def file_check():
    relation = {}
    with open("F:/project_dir/merge.txt") as mf:
        line = mf.readline()
        while line:
            line = line.strip('\n')
            size = line.split("\t")
            relation.setdefault(size[0], size[1])
            line = mf.readline()
        mf.close()

    with open("F:/project_dir/gen_data.txt") as genf:
        line = genf.readline()
        while line:
            line = line.strip('\n')
            size = line.split("\t")
            # if(size[1] not in relation):
            #     print(line)
            if(relation.get(size[1]) and relation[size[1]] != size[2]):
                sql = "UPDATE item_user_map SET user_id = "+relation[size[1]]+" WHERE id = "+size[0]+";"
                print(sql)

            line = genf.readline()
        genf.close()


# 数据缺失检查
def lack_check():
    relation = {}
    with open("F:/project_dir/gen_data.txt") as mf:
        line = mf.readline()
        while line:
            line = line.strip('\n')
            size = line.split("\t")
            relation.setdefault(size[1], size[2])
            line = mf.readline()
        mf.close()

    with open("F:/project_dir/merge.txt") as genf:
        line = genf.readline()
        query_sql = "select * from item_sku where item_id in ("
        while line:
            line = line.strip('\n')
            size = line.split("\t")

            if (size[0] not in relation):
                query_sql += size[0]+","
                sql = "INSERT INTO `item_user_map` (item_id,user_id,warehouse_type,status) VALUES (" + size[0] + "," + size[1] + "," + size[2] + ",0);"
                print(sql)
            line = genf.readline()

        # print(query_sql[:-1]+")")
        genf.close()


def wrong_check():
    relation = {}
    with open("F:/project_dir/merge.txt") as mf:
        line = mf.readline()
        while line:
            line = line.strip('\n')
            size = line.split("\t")
            relation.setdefault(size[0], size[1])
            line = mf.readline()
        mf.close()

    with open("F:/project_dir/gen_data.txt") as genf:
        line = genf.readline()
        while line:
            line = line.strip('\n')
            size = line.split("\t")

            if (size[1] not in relation):
                print(size[1])
            line = genf.readline()

        # print(query_sql[:-1]+")")
        genf.close()


def read_csv():
    # 1.获取用户关系映射
    with open("C:/Users/cuijiabin/Desktop/接口参数/口碑代码/175.txt", encoding="utf8") as rf:
        line = rf.readline()
        while line:
            line = line.strip('\n')
            size = line.split(",")
            print(size[0])
            # for i in range(len(size)):
            #     print(size[0])
            line = rf.readline()
        rf.close()
    # 2.读取原生数据

if __name__ == "__main__":
    # merge_file()
    file_check()
    # lack_check()
    # wrong_check()
    # read_csv()

    # TODO 换成python来处理？ 数据导出脚本
    # mysql -h10.1.3.33 -upop_cuijiabin -p8dtx5EOUZASc# -e "select distinct sku.item_id, spu.supplier_id, spu.warehouse_type from db_pop.item_spu spu left join  db_pop.item_sku sku on sku.spu_id = spu.id where spu.warehouse_type in (3,5,7) order by sku.item_id asc" >.\origin_data.txt
    # mysql -h10.1.3.33 -upop_cuijiabin -p8dtx5EOUZASc# -e "SELECT mia_supplier_id, pop_admin_id FROM vr_pop.pop_customer_supplier" >.\relation.txt
    # mysql -h10.1.3.33 -upop_cuijiabin -p8dtx5EOUZASc# -e "select * from mia_mirror.item_user_map where warehouse_type in(3,5,7) and status = 0 order by item_id asc" >.\gen_data.txt