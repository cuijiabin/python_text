import pymysql
from string import Template
from collections import Counter

global_spu_map = {
    5565870: 5676564,
    2485877: 5676564,
    2486004: 5676563,
    5767854: 5676562,
    5565871: 5676561,
    5766953: 5676564,
    2526700: 5676560,
    5766183: 5676559,
    5565877: 5676558
}

global_multi_spu_map = {
    5766952: [5096238, 5096239],
    5776537: [5096239, 5096240],
    5776042: [5096235, 5096236]
}


def get_mia_cursor(db_name="mia"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_superior_order_list():
    cur = get_mia_cursor("mia")

    sql = "SELECT tmp.user_id  AS userId , count(tmp.superior_order_code) as orderCount,GROUP_CONCAT(tmp.superior_order_code) as orderCodeList,  " + \
          "sum(tmp.orderItemNum) as orderItemNum,tmp.dst_info as dstInfo from  " + \
          "(SELECT o.superior_order_code, o.user_id, count(oi.id) AS orderItemNum,sum(oi.pay_price) AS pay_price, " + \
          "  CONCAT(o.user_id,o.dst_name,o.dst_mobile,o.dst_province,o.dst_city,o.dst_area,o.dst_street,o.dst_address) as dst_info " + \
          "FROM orders o LEFT JOIN order_item oi ON o.id = oi.order_id " + \
          "WHERE o.order_time > '2021-01-05 14:00' and o.`status` < 6  and o.channel = 211 " + \
          "AND oi.spu_id IN ( 5565870, 2485877, 2486004, 5767854, 5565871, 5766953, 5766952, 5776537, 2526700, 5766183, 5565877, 5776042) " + \
          "GROUP BY o.superior_order_code ORDER BY o.user_id ASC) tmp " + \
          "GROUP BY tmp.dst_info having orderItemNum >=8 ORDER BY orderCount DESC"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()

    return rows


def get_gift_info(superior_order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "select spu_id,count(id) DIV 4 as num from order_item WHERE order_id in "
        "(select id from orders WHERE superior_order_code in ($superior_order_code)) "
        "and spu_id in (5565870, 2485877, 2486004, 5767854, 5565871, 5766953, 5766952, 5776537, 2526700, 5766183, 5565877, 5776042) "
        "GROUP BY spu_id")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_base_info(superior_order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT DISTINCT oc.open_order_id AS open_order_id, o.superior_order_code, o.transaction_id, o.dst_name,o.dst_mobile,"
        "o.dst_province,o.dst_city,o.dst_area,o.dst_street,o.dst_address,o.warehouse_id,o.pay_mode "
        "from orders o LEFT JOIN open_order_channel oc on o.superior_order_code = oc.superior_order_code "
        "WHERE o.superior_order_code = $superior_order_code")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return result_data[0]
    return None


def get_sub_base_info(superior_order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "select GROUP_CONCAT(order_code) from orders "
        "WHERE superior_order_code in ($superior_order_code)")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return result_data[0][0]
    return None


def get_gift_result():
    superior_order_list = get_superior_order_list()
    for superior_order in superior_order_list:
        superior_order_code = superior_order["orderCodeList"]
        s_list = list(map(lambda x: "'" + str(x) + "'", superior_order_code.split(",")))
        s_order_code = s_list[0]
        base_info = get_base_info(s_order_code)
        if base_info[0] is None:
            continue
        code_lists = ','.join(s_list)
        # sub_info = get_sub_base_info(code_lists)
        # convert_sub_info = sub_info.replace(",", "、")
        # t_code = base_info[0]
        # t_code = t_code + "B"
        # os_list = sub_info.split(",")
        # for os in os_list:
        #     print(os, ",", "2021-1-5抖音直播间购买拉拉裤/纸尿裤同地址超过8包补发赠品，补发新订单号抖音号：" + t_code + "； 同地址订单号：" + convert_sub_info)

        spu_list = get_gift_info(code_lists)
        for spu in spu_list:
            spu_id = spu["spu_id"]
            spu_num = spu["num"]
            if global_spu_map.get(spu_id) is not None:
                target_spu_id = global_spu_map[spu_id]
                convert_result(base_info, target_spu_id, spu_num)
            else:
                spu_id_list = global_multi_spu_map.get(spu_id)
                for target_spu_id in spu_id_list:
                    convert_result(base_info, target_spu_id, spu_num * 2)


def convert_result(base_info, target_spu_id, num):
    t_code = base_info[0]
    transaction_id = base_info[2]
    t_code = t_code + "B"
    transaction_id = transaction_id + "B"
    result = [t_code, transaction_id, base_info[3], base_info[4], base_info[5], base_info[6], base_info[7],
              base_info[8], base_info[9], "0", "0", "0", str(target_spu_id), "0", str(num), "0", "", "",
              "", "", "", "",
              str(base_info[11])]
    print(','.join(result))


def get_spu_info(superior_order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT "
        "IF(item_info.spu_id=0,0,1) AS is_spu, "
        "IF(item_info.spu_id=0, item_info.item_id, item_info.spu_id) AS item_id, "
        "IF(item_info.spu_id=0, item_info.qty, ROUND(item_info.qty/item_info.item_amount)) AS item_count, "
        "sum(item_info.pay_price) AS pay_price "
        "FROM ( "
        "SELECT oi.spu_id, oi.item_id,ssr.item_amount,count(oi.id) AS qty,sum(oi.pay_price) AS pay_price "
        "FROM orders o "
        "INNER JOIN order_item oi ON  o.id=oi.order_id "
        "LEFT JOIN spu_sku_relation ssr ON ssr.spu_id=oi.spu_id AND ssr.item_id=oi.item_id "
        "WHERE o.superior_order_code in( '$superior_order_code') AND o.status != 6 "
        "AND oi.spu_id in (5137432,5863223,5946383,6034604,5948456,5948454,5894922,5894921) "
        "GROUP BY oi.spu_id,oi.item_id "
        ") item_info "
        "GROUP BY item_info.spu_id "
        "ORDER BY item_id ASC")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


cal_map = {
    5137432: [5009094, 5852376, 5852376, 5852376, 5852376, 5852377, 5852377, 5852377, 5852377, 5852377, 5852378,
              5852378, 5852378, 5852378, 5852378, 5852381, 5852381, 5852381, 5852381, 5852381],
    5863223: [5852381, 5852381, 5852381, 5852381, 5852381, 5876100, 5876100, 5876100, 5876100, 5876100],
    5946383: [5852381, 5852381, 5852381, 5852381, 5852381],
    6034604: [5852381, 5852381, 5852381, 5852381, 5852381, 5852381, 5852381],
    5948456: [5852377, 5852377, 5852377, 5852377, 5852377, 5852381],
    5948454: [5852377, 5852377, 5852377, 5852377, 5852377, 5852381],
    5894921: [5852378, 5852378, 5852378, 5852378, 5852378, 5852381],
    5894922: [5852376, 5852376, 5852376, 5852376, 5852376, 5852381]
}

if __name__ == '__main__':
    ss = ['202106182435525604', '202106182435526095', '202106182435528773', '202106182435529264', '202106182435530593',
          '202106182435531085', '202106182435531824', '202106182435532353', '202106182435533155', '202106182435534775',
          '202106182435536765', '202106182435540015', '202106182435542114', '202106182435542665', '202106182435543493',
          '202106182435544675', '202106182435545654', '202106182435546204', '202106182435549685', '202106182435554404',
          '202106182435554604', '202106182435555865', '202106182435562793', '202106182435566125', '202106182435568113',
          '202106182435570414', '202106182435571485', '202106182435572733', '202106182435573793', '202106182435577105',
          '202106182435580165', '202106182435581914', '202106182435586494', '202106182435588123', '202106182435592787',
          '202106182435596106', '202106182435602558', '202106182435606758', '202106182435608197', '202106182435625877',
          '202106182435627656', '202106182435629796', '202106182435631857', '202106182435633977', '202106182435634597',
          '202106182435634716', '202106182435634756', '202106182435636668', '202106182435639217', '202106182435642436',
          '202106182435643887', '202106182435646147', '202106182435646746', '202106182435651456', '202106182435653267',
          '202106182435653378', '202106182435653477', '202106182435654226', '202106182435656157', '202106182435656368',
          '202106182435656446', '202106182435657077', '202106182435659818', '202106182435660167', '202106182435661718',
          '202106182435662416', '202106182435662578', '202106182435662796', '202106182435664228', '202106182435666698',
          '202106182435668128', '202106182435670136', '202106182435698406', '202106182435703047', '202106182435704678',
          '202106182435705766', '202106182435709117', '202106182435709517', '202106182435713876', '202106182435714697',
          '202106182435716847', '202106182435717588', '202106182435721257', '202106182435722038', '202106182435723788',
          '202106182435727718', '202106182435730558', '202106182435730808', '202106182435731108', '202106182435734636',
          '202106182435738698', '202106182435739028', '202106182435746747', '202106182435746908', '202106182435746986',
          '202106192435757432', '202106192435761781', '202106192435761800', '202106192435768251', '202106192435770910',
          '202106192435772702', '202106192435774050', '202106192435774210', '202106192435775912', '202106192435782902',
          '202106192435783971', '202106192435795780', '202106192435796231', '202106192435797372', '202106192435802330',
          '202106192435803240', '202106192435804440', '202106192435805221', '202106192435806431', '202106192435807200',
          '202106192435807262', '202106192435807412', '202106192435807701', '202106192435808640', '202106192435815411',
          '202106192435816531', '202106192435818390', '202106192435818871', '202106192435819300', '202106192435820160',
          '202106192435820501', '202106192435820810', '202106192435820850', '202106192435825770', '202106192435826182',
          '202106192435829421', '202106192435829442', '202106192435829470', '202106192435830451', '202106192435830802',
          '202106192435831030', '202106192435835980', '202106192435836012', '202106192435838762', '202106192435839700',
          '202106192435840471', '202106192435841972', '202106192435850615', '202106192435853603', '202106192435854713',
          '202106192435856003', '202106192435856924', '202106192435858553', '202106192435862124', '202106192435866574',
          '202106192435871604', '202106192435872644', '202106192435873975', '202106192435876604', '202106192435877054',
          '202106192435877894', '202106192435879263', '202106192435881843', '202106192435883215', '202106192435886874',
          '202106192435893344', '202106192435893574', '202106192435895233', '202106192435895735', '202106192435900233',
          '202106192435900695', '202106192435902565', '202106192435917545', '202106192435924323', '202106192435925737',
          '202106192435926607', '202106192435927247', '202106192435927566', '202106192435936797', '202106192435942956',
          '202106192435946457', '202106192435949218', '202106192435949976', '202106192435952706', '202106192435954187',
          '202106192435954866', '202106192435955388', '202106192435958606', '202106192435962347', '202106192435962606',
          '202106192435963366', '202106192435967607', '202106192435968077', '202106192435968896', '202106192435969156',
          '202106192435969998', '202106192435970476', '202106192435971318', '202106192435971408', '202106192435972386',
          '202106192435972568', '202106192435972708', '202106192435974858', '202106192435976117', '202106192435976898',
          '202106192435977338', '202106192435978917', '202106192435979426', '202106202435980472', '202106202435980562',
          '202106202435981242', '202106202435983372', '202106202435984620', '202106202435984810', '202106202435988090',
          '202106202435994181', '202106202435994850', '202106202435995492', '202106202435999692', '202106202436002551',
          '202106202436002632', '202106202436002730', '202106202436002761', '202106202436003050', '202106202436003400',
          '202106202436004081', '202106202436004500', '202106202436005850', '202106202436008390', '202106202436009592',
          '202106202436010170', '202106202436011422', '202106202436011861', '202106202436012071', '202106202436012342',
          '202106202436013980', '202106202436016102', '202106202436018612', '202106202436019101', '202106202436020510',
          '202106202436021080', '202106202436022482', '202106202436022551', '202106202436023050', '202106202436023742',
          '202106202436025330', '202106202436025590', '202106202436025662', '202106202436026951', '202106202436028280',
          '202106202436028721', '202106202436029791', '202106202436030242', '202106202436030680', '202106202436031792',
          '202106202436032042', '202106202436032830', '202106202436033560', '202106182435524993', '202106182435537765',
          '202106182435540463', '202106182435553743', '202106182435555893', '202106182435559535', '202106182435563114',
          '202106182435566074', '202106182435594496', '202106182435598627', '202106182435607677', '202106182435638826',
          '202106182435649096', '202106182435652018', '202106182435653818', '202106182435660367', '202106182435666596',
          '202106182435709436', '202106182435724547', '202106182435724987', '202106182435733256', '202106182435738127',
          '202106182435739017', '202106182435739146', '202106182435739518', '202106182435746786', '202106192435757521',
          '202106192435764221', '202106192435798160', '202106192435800261', '202106192435811781', '202106192435832890',
          '202106192435833112', '202106192435834041', '202106192435843191', '202106192435847274', '202106192435851824',
          '202106192435863364', '202106192435881893', '202106192435890514', '202106192435894253', '202106192435899165',
          '202106192435935916', '202106192435940376', '202106192435949446', '202106192435950747', '202106192435967328',
          '202106192435969338', '202106192435972508', '202106192435978516', '202106192435979028', '202106192435980278',
          '202106202435991512', '202106202435996762', '202106202436001692', '202106202436027950', '202106202436030371',
          '202106182435537173', '202106182435553343', '202106182435659027', '202106182435668308', '202106192435832171',
          '202106192435894493', '202106202436001832', '202106182435542614', '202106182435546384', '202106182435550804',
          '202106182435558083', '202106182435558664', '202106182435573754', '202106182435574084', '202106182435664196',
          '202106182435701698', '202106192435760160', '202106192435903205', '202106192435909863', '202106192435922324',
          '202106192435953538', '202106202435987440', '202106202436013502', '202106202436017072', '202106202436020030',
          '202106202436021360', '202106182435527155', '202106182435527935', '202106182435530565', '202106182435530985',
          '202106182435531143', '202106182435531844', '202106182435535164', '202106182435535654', '202106182435545504',
          '202106182435556145', '202106182435556284', '202106182435558533', '202106182435558973', '202106182435570273',
          '202106182435586505', '202106182435589476', '202106182435589628', '202106182435589986', '202106182435595077',
          '202106182435597777', '202106182435599047', '202106182435600037', '202106182435600447', '202106182435606768',
          '202106182435608606', '202106182435611426', '202106182435621396', '202106182435626228', '202106182435627376',
          '202106182435627477', '202106182435631718', '202106182435632976', '202106182435634357', '202106182435635996',
          '202106182435637376', '202106182435643607', '202106182435643918', '202106182435646878', '202106182435646887',
          '202106182435655788', '202106182435658817', '202106182435660018', '202106182435661497', '202106182435662876',
          '202106182435664397', '202106182435667128', '202106182435667248', '202106182435669888', '202106182435670556',
          '202106182435697688', '202106182435706177', '202106182435712706', '202106182435713166', '202106182435720827',
          '202106182435726847', '202106182435728148', '202106182435731296', '202106182435733758', '202106182435734176',
          '202106192435750522', '202106192435757910', '202106192435761862', '202106192435762461', '202106192435764380',
          '202106192435772641', '202106192435775862', '202106192435781431', '202106192435794881', '202106192435796542',
          '202106192435797001', '202106192435797262', '202106192435797281', '202106192435797340', '202106192435800451',
          '202106192435800591', '202106192435802650', '202106192435803272', '202106192435804920', '202106192435808141',
          '202106192435809572', '202106192435812171', '202106192435818010', '202106192435819812', '202106192435820550',
          '202106192435821071', '202106192435821751', '202106192435822241', '202106192435822842', '202106192435830590',
          '202106192435830661', '202106192435832020', '202106192435835210', '202106192435845522', '202106192435871133',
          '202106192435872693', '202106192435875194', '202106192435875703', '202106192435880983', '202106192435890555',
          '202106192435898975', '202106192435900944', '202106192435910753', '202106192435919824', '202106192435930486',
          '202106192435937827', '202106192435943677', '202106192435952156', '202106192435962628', '202106192435963326',
          '202106192435964516', '202106192435964657', '202106192435972307', '202106192435980157', '202106202435985310',
          '202106202435986841', '202106202435988470', '202106202435992280', '202106202435997990', '202106202436000720',
          '202106202436001530', '202106202436001970', '202106202436009551', '202106202436009762', '202106202436009770',
          '202106202436017871', '202106202436020372', '202106202436021150', '202106202436023312', '202106202436026450',
          '202106202436026470', '202106202436027101', '202106202436027642', '202106202436029311', '202106202436029412',
          '202106202436031062', '202106202436031521', '202106182435527463', '202106182435555375', '202106182435556844',
          '202106182435560225', '202106182435562884', '202106182435570995', '202106182435582045', '202106182435595727',
          '202106182435599928', '202106182435602017', '202106182435607488', '202106182435642366', '202106182435642447',
          '202106182435644056', '202106182435659527', '202106182435667436', '202106182435727678', '202106182435746556',
          '202106182435746758', '202106192435794782', '202106192435797531', '202106192435797650', '202106192435804330',
          '202106192435806121', '202106192435806462', '202106192435811552', '202106192435813251', '202106192435818800',
          '202106192435825312', '202106192435825991', '202106192435831420', '202106192435842042', '202106192435842550',
          '202106192435860933', '202106192435872235', '202106192435875385', '202106192435876335', '202106192435880275',
          '202106192435889844', '202106192435899205', '202106192435901014', '202106192435919505', '202106192435928296',
          '202106192435965156', '202106202435985602', '202106202435994241', '202106202436009081', '202106202436012011',
          '202106202436027250', '202106202436033522', '202106182435573745', '202106182435591157', '202106182435607558',
          '202106182435668167', '202106192435764742', '202106192435786081', '202106192435811452', '202106192435815570',
          '202106192435833460', '202106192435878003', '202106192435914223', '202106192435956007', '202106192435962368',
          '202106192435964538', '202106192435976757', '202106202436008162', '202106202436008680', '202106202436012410']
    for s in ss:
        spu_info = get_spu_info(s)
        pay_price = 0.0
        spu_desc = ""
        gift_sku = []
        for spp in spu_info:
            pay_price += spp["pay_price"]
            item_id = spp["item_id"]
            num = int(spp["item_count"])
            spu_desc += str(spp["item_id"]) + ": " + str(num) + ", "
            gf = cal_map.get(item_id)
            for i in range(num):
                for g in gf:
                    gift_sku.append(g)

        print(spu_desc + "#" + str(pay_price) + "#" + str(dict(Counter(gift_sku))) + "#" + str(len(gift_sku)))