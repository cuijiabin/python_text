# coding=utf-8
import json
from string import Template
import util as bm
import util.mia_db as mb


# 获取在线开发信息功能
def get_base_visual_info(f_id):
    sql_tmp = Template(
        "SELECT * "
        "FROM base_visualdev "
        "WHERE F_Id = '$F_Id'"
    )
    sql = sql_tmp.substitute(F_Id=f_id)

    return bm.get_cctd_db_data(sql)


# 获取在线开发信息列表
def get_base_visual_list():
    sql_tmp = Template(
        "SELECT * "
        "FROM base_visualdev "
    )
    sql = sql_tmp.substitute()

    return bm.get_cctd_db_data(sql)


# 分析单个表单信息
def analyse_visual_form(visual_info):
    if 'F_FormData' not in visual_info or visual_info['F_FormData'] is None:
        return
    form_data = json.loads(visual_info['F_FormData'])
    form_fields = form_data['fields']
    point_data = []
    for field in form_fields:
        other = field['__config__']
        if 'dataType' in other:
            if other['dataType'] == 'dictionary' and field['props']['value'] != 'enCode':
                point_data.append({
                    "jnpfKey": other['jnpfKey'],
                    "label": other['label'],
                    "tag": other['label'],
                    "dataType": other['dataType'],
                    "dictionaryType": other['dictionaryType'],
                    "propsUrl": other['propsUrl'],
                    "props": field['props']
                })
            # print(other)
            # point_data.append({
            #     "jnpfKey": other['jnpfKey'],
            #     "label": other['label'],
            #     "tag": other['label'],
            #     "dataType": other['dataType'],
            #     "dictionaryType": other['dictionaryType'],
            #     "propsUrl": other['propsUrl'],
            #     "props": field['props']
            # })

    if len(point_data) > 0:
        print(visual_info['F_FullName'])
        for point in point_data:
            print(point)


# 数据库字段分析处理
def analyse_visual_field(visual_info):
    if 'F_FormData' not in visual_info or visual_info['F_FormData'] is None:
        return
    form_data = json.loads(visual_info['F_FormData'])
    form_fields = form_data['fields']
    bmp_map = dict()
    table_set = set()
    for field in form_fields:
        if '__vModel__' not in field:
            continue

        column_name = field['__vModel__']
        other = field['__config__']
        if 'tableName' in other:
            table_name = other['tableName']
            bmp_map[table_name + "#" + column_name] = {
                "jnpfKey": other['jnpfKey'],
                "label": other['label'],
                "tag": other['label'],
                "tableName": other['tableName']
            }
            table_set.add(table_name)

    print(visual_info['F_FullName'])
    # print(table_set)

    cur = bm.get_cctd_cursor()
    for table_name in table_set:
        column_list = mb.get_columns(table_name, cur)
        # print(column_list)
        for key in column_list:
            column_key = key.split("\t")[0]
            column_key = table_name + "#" + column_key
            if column_key not in bmp_map:
                print(column_key + " 沒有被表单使用")
    cur.close()


# 单个分析
def analyse_visual_form_id(f_id):
    visual_info = get_base_visual_info(f_id)
    analyse_visual_form(visual_info[0])
    # analyse_visual_field(visual_info[0])


# 批量分析
def analyse_visual_form_list():
    visual_info = get_base_visual_list()
    for info in visual_info:
        analyse_visual_form(info)
        # analyse_visual_field(info)


if __name__ == '__main__':
    analyse_visual_form_id("549915349563297925")
    # analyse_visual_form_list()
