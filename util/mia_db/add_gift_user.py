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
        "AND oi.spu_id in (6067463) "
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


def get_all_info(superior_order_code):
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
        "AND oi.spu_id in (5793597, 5793596, 5793595, 5793594, 5793593, 5793592, 5793591, 5565870, 2485877, 2486004, 5767854, 5928012, 5894017, 5766183, 5565877) "
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
    6067463: [5565956, 5565956, 5641519]
}

if __name__ == '__main__':
    # print("订单号,交易流水号,收货人,手机号,省,市,区,街道,地址,订单总支付金额,总邮费,总税费,商品ID,单个销售价,数量,单个税费,仓库id,身份证号,真实姓名,身份证正面,身份证反面,客户备注,支付方式")
    # get_gift_result()

    ss = ['202108042444001483', '202108042444001523', '202108042444001613', '202108042444002083', '202108042444002513',
          '202108042444002673', '202108042444002283', '202108042444002633', '202108042444002403', '202108042444002243',
          '202108042444001993', '202108042444002333', '202108042444002623', '202108042444002253', '202108042444002313',
          '202108042444002223', '202108042444002153', '202108042444002713', '202108042444002383', '202108042444002233',
          '202108042444001963', '202108042444002103', '202108042444002033', '202108042444002143', '202108042444002373',
          '202108042444002013', '202108042444002363', '202108042444002493', '202108042444001973', '202108042444002043',
          '202108042444002443', '202108042444002523', '202108042444002723', '202108042444002553', '202108042444002293',
          '202108042444002453', '202108042444002133', '202108042444002193', '202108042444003826', '202108042444003156',
          '202108042444003266', '202108042444003316', '202108042444003576', '202108042444003176', '202108042444003416',
          '202108042444003146', '202108042444003926', '202108042444003546', '202108042444003286', '202108042444003186',
          '202108042444003226', '202108042444003626', '202108042444003366', '202108042444003346', '202108042444003716',
          '202108042444003276', '202108042444003696', '202108042444003636', '202108042444003426', '202108042444003706',
          '202108042444006336', '202108042444003206', '202108042444003686', '202108042444004896', '202108042444004546',
          '202108042444004676', '202108042444004296', '202108042444004496', '202108042444005776', '202108042444005766',
          '202108042444005356', '202108042444012486', '202108042444006666', '202108042444007326', '202108042444006426',
          '202108042444007096', '202108042444006396', '202108042444006896', '202108042444007146', '202108042444008146',
          '202108042444007996', '202108042444009456', '202108042444009386', '202108042444009126', '202108042444009586',
          '202108042444010486', '202108042444013626', '202108042444010276', '202108042444012336', '202108042444012186',
          '202108042444012296', '202108042444012556', '202108042444011916', '202108042444012416', '202108042444012626',
          '202108042444013496', '202108042444013736', '202108042444013276', '202108042444013636', '202108042444013666',
          '202108042444013566', '202108042444013976', '202108042444013806', '202108042444015306', '202108042444015056',
          '202108042444015126', '202108042444015146', '202108042444015246', '202108042444015606', '202108042444015336',
          '202108042444015566', '202108042444015996', '202108042444015966', '202108042444016046', '202108042444016006',
          '202108042444016186', '202108042444018416', '202108042444016056', '202108042444016286', '202108042444018526',
          '202108042444018516', '202108042444018926', '202108042444019166', '202108042444018786', '202108042444019126',
          '202108042444018436', '202108042444018456', '202108042444019196', '202108042444020506', '202108042444020656',
          '202108042444020286', '202108042444022936', '202108042444022396', '202108042444022516', '202108042444028046',
          '202108042444022776', '202108042444022826', '202108042444022876', '202108042444022836', '202108042444023126',
          '202108042444024626', '202108042444024646', '202108042444024466', '202108042444024796', '202108042444024816',
          '202108042444024576', '202108042444026726', '202108042444026526', '202108042444026466', '202108042444026996',
          '202108042444026706', '202108042444026696', '202108042444026606', '202108042444026516', '202108042444026716',
          '202108042444033896', '202108042444033576', '202108042444027796', '202108042444027776', '202108042444027916',
          '202108042444028406', '202108042444027996', '202108042444027946', '202108042444030046', '202108042444029956',
          '202108042444030176', '202108042444030596', '202108042444031816', '202108042444031746', '202108042444031266',
          '202108042444031616', '202108042444031696', '202108042444031246', '202108042444032346', '202108042444032476',
          '202108042444032286', '202108042444032766', '202108042444032616', '202108042444032276', '202108042444032376',
          '202108042444032556', '202108042444032856', '202108042444033696', '202108042444033466', '202108042444033636',
          '202108042444035026', '202108042444035066', '202108042444036306', '202108042444037066', '202108042444037206',
          '202108042444036916', '202108042444037046', '202108042444037096', '202108042444037666', '202108042444038246',
          '202108042444038536', '202108042444038266', '202108042444038166', '202108042444038456', '202108042444039906',
          '202108042444040156', '202108042444040106', '202108042444041876', '202108042444041846', '202108042444042106',
          '202108042444043466', '202108042444042556', '202108042444042586', '202108042444042596', '202108042444044526',
          '202108042444044246', '202108042444044276', '202108042444045056', '202108042444045086', '202108042444045006',
          '202108042444045366', '202108042444045246', '202108042444046576', '202108042444046506', '202108042444046466',
          '202108042444046456', '202108042444046496', '202108042444048046', '202108042444047556', '202108042444047816',
          '202108042444047706', '202108042444047836', '202108042444047606', '202108042444048096', '202108042444048036',
          '202108042444049136', '202108042444049146', '202108042444048816', '202108042444049096', '202108042444049816',
          '202108042444049466', '202108042444050816', '202108042444050506', '202108042444050756', '202108042444050576',
          '202108042444051466', '202108042444051366', '202108042444051456', '202108042444051956', '202108042444051876',
          '202108042444052526', '202108042444052706', '202108042444052666', '202108042444054106', '202108042444053096',
          '202108042444053126', '202108042444054246', '202108042444054006', '202108042444053966', '202108042444054186',
          '202108042444053976', '202108042444054476', '202108042444054906', '202108042444055396', '202108042444054766',
          '202108042444059846', '202108042444057156', '202108042444058236', '202108042444058286', '202108042444058426',
          '202108042444058346', '202108042444058626', '202108042444060106', '202108042444060366', '202108042444060406',
          '202108042444061486', '202108042444061616', '202108042444063356', '202108042444063066', '202108042444063276',
          '202108042444063246', '202108042444063256', '202108042444063706', '202108042444063776', '202108042444063896',
          '202108042444065046', '202108042444064666', '202108042444064706', '202108042444064916', '202108042444064576',
          '202108042444065406', '202108042444072326', '202108042444066206', '202108042444066316', '202108042444066306',
          '202108042444066366', '202108042444066736', '202108042444066436', '202108042444066216', '202108042444066376',
          '202108042444066416', '202108042444066226', '202108042444066916', '202108042444067226', '202108042444066786',
          '202108042444067996', '202108042444068136', '202108042444067966', '202108042444068326', '202108042444067876',
          '202108042444068216', '202108042444068416', '202108042444068686', '202108042444069416', '202108042444069596',
          '202108042444069766', '202108042444069506', '202108042444069556', '202108042444069376', '202108042444069586',
          '202108042444069986', '202108042444070976', '202108042444070636', '202108042444070946', '202108042444070776',
          '202108042444070726', '202108042444070906', '202108042444070706', '202108042444072056', '202108042444070986',
          '202108042444070506', '202108042444071006', '202108042444070676', '202108042444072426', '202108042444072526',
          '202108042444072586', '202108042444072646', '202108042444072866', '202108042444072486', '202108042444073226',
          '202108042444074266', '202108042444074876', '202108042444074656', '202108042444074756', '202108042444074446',
          '202108042444074676', '202108042444074376', '202108042444074326', '202108042444074556', '202108042444074816',
          '202108042444075146', '202108042444074916', '202108042444076096', '202108042444075726', '202108042444076046',
          '202108042444075976', '202108042444075876', '202108042444076246', '202108042444076896', '202108042444077446',
          '202108042444076936', '202108042444076966', '202108042444077216', '202108042444076986', '202108042444077076',
          '202108042444077326', '202108042444077486', '202108042444077896', '202108042444077856', '202108042444077606',
          '202108042444077796', '202108042444077656', '202108042444077936', '202108042444078936', '202108042444078106',
          '202108042444078916', '202108042444079136', '202108042444078786', '202108042444078856', '202108042444078836',
          '202108042444079596', '202108042444078656', '202108042444079696', '202108042444079306', '202108042444079806',
          '202108042444080026', '202108042444081036', '202108042444080666', '202108042444080706', '202108042444080486',
          '202108042444080626', '202108042444080576', '202108042444080366', '202108042444080506', '202108042444080646',
          '202108042444080756', '202108042444080946', '202108042444081436', '202108042444081216', '202108042444082506',
          '202108042444082776', '202108042444082146', '202108042444082226', '202108042444082546', '202108042444083606',
          '202108042444082176', '202108042444083096', '202108052444085000', '202108052444084610', '202108052444084910',
          '202108052444084870', '202108052444086140', '202108052444086090', '202108052444086240', '202108092445257090',
          '202108052444086700', '202108052444086910', '202108052444087410', '202108052444087610', '202108052444087490',
          '202108052444089090', '202108052444088100', '202108052444087960', '202108052444087520', '202108052444087900',
          '202108052444089140', '202108052444088450', '202108052444089490', '202108052444089730', '202108052444089540',
          '202108052444089620', '202108052444090610', '202108052444092210', '202108052444090740', '202108052444090920',
          '202108052444090600', '202108052444090860', '202108052444092080', '202108052444092260', '202108052444091720',
          '202108052444091450', '202108052444091750', '202108052444091490', '202108052444091600', '202108052444093140',
          '202108052444094530', '202108052444093790', '202108052444095530', '202108052444095560', '202108052444095790',
          '202108052444096760', '202108052444096740', '202108052444097260', '202108052444098190'
          ]
    for s in ss:
        # spu_info = get_spu_info(s)
        spu_info = get_all_info(s)
        pay_price = 0.0
        spu_desc = ""
        gift_sku = []
        has_gift_sku = []
        for spp in spu_info:
            pay_price += spp["pay_price"]
            item_id = spp["item_id"]
            num = int(spp["item_count"])
            spu_desc += str(spp["item_id"]) + ": " + str(num) + ", "
            gf = cal_map.get(item_id)
            for i in range(num):
                if gf is None or len(gf) < 1:
                    has_gift_sku.append(item_id)
                else:
                    for g in gf:
                        gift_sku.append(g)

        print(str(dict(Counter(has_gift_sku))) + "#" + str(pay_price) + "#" + str(len(has_gift_sku)))
