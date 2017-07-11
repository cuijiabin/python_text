# coding=gbk
import pymysql
import json


def get_connection():
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='rap_db', port=3306, charset='utf8')
    cur = conn.cursor()
    cur.execute(
        'SELECT tr.parameter_id, tp.`name`,tp.identifier,tp.data_type  from  tb_request_parameter_list_mapping tr LEFT JOIN tb_parameter tp ON tr.parameter_id = tp.id WHERE action_id = 155 ORDER BY tp.`name`')
    data = cur.fetchall()
    dict_json = {}
    for d in data:
        print("参数ID:" + str(d[0]) + "  ;参数名称:" + d[1] + " 标示:" + d[2] + " 数据类型：" + d[3])
        if (d[3] == 'string'):
            dict_json[d[2]] = "input_str"
        if (d[3] == 'number'):
            dict_json[d[2]] = "input_num"
    print(json.dumps(dict_json))

    cur.close()
    conn.close()


get_connection()


def genScript():
    conn = pymysql.connect(host='10.1.3.42', user='liuhan', passwd='s79dliuhan', port=3306, charset='utf8')
    cur = conn.cursor()
    cur.execute("select distinct sku.item_id, pcs.pop_admin_id as user_id, spu.warehouse_type \
	         from db_pop.item_spu spu \
             left join  db_pop.item_sku sku on sku.spu_id = spu.id \
             left join  vr_pop.pop_customer_supplier pcs on pcs.mia_supplier_id = spu.supplier_id \
             where spu.warehouse_type in (3,5,7)")
    data = cur.fetchall()
    for d in data:
        print("参数ID:" + str(d[0]) + "  ;参数名称:" + d[1] + " 标示:" + d[2])

# genScript()