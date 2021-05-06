import datetime

from geopy import Baidu

from applet_background.link_config import con_mysql


def check_login_authentication(user_phone, pass_word):
    '''
    验证登录函数
    :param user_phone: 用户手机号
    :param pass_word: 用户密码
    :return: 验证成功返回True 否则False
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute("select count(1), passWord from manager_list where phoneNumber = %s", user_phone)
    count = cursor.fetchone()
    cursor.close()
    con_mysql_connect.close()
    if count[0] == 1:
        if count[1] == str(pass_word):
            return True
        else:
            return False
    else:
        return False


def check_user_auth_level(user_phone):
    '''

    :param user_phone:  用户手机号
    :return: 用户等级
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute("select level, agentId, agentName from manager_list where phoneNumber = %s", user_phone)
    level = cursor.fetchone()
    cursor.close()
    con_mysql_connect.close()
    return level


def drop_down_list_data(user_phone):
    '''
    首页 下拉列表数据 get 请求
    :return:
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    dict_ = dict()
    if check_user_auth_level(user_phone=user_phone)[0] == '0':
        search_list = ['agentName', 'hosName', 'hosDepartM']
        for param in search_list:
            cursor.execute("select  %s  from hos_list GROUP BY %s" % (param, param))
            data = cursor.fetchall()
            print(data)
            dict_[param] = [i[0] for i in data]
    else:
        search_list = ['hosName', 'hosDepartM']
        cursor.execute("select  agentName  from manager_list where phoneNumber = %s " % user_phone)
        agent_data = cursor.fetchone()
        agent_name = agent_data[0]
        for param in search_list:
            cursor.execute("select  %s  from hos_list where agentName = '%s' GROUP BY %s" % (param, agent_name, param))
            data = cursor.fetchall()
            dict_[param] = [i[0] for i in data]
    print(dict_)
    cursor.close()
    con_mysql_connect.close()
    return dict_


def drop_down_list_by_param(param_dict):
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    str_search = ' where '
    for k, v in param_dict.items():
        if v is None or len(v) == 0:
            pass
        else:
            str_search += str('%s' + ' = ' + '"''%s''"' + ' and ') % (k, v)
    param_search = ['agentName', 'province', 'city', 'area', 'hosId', 'hosDepartM']
    dict_data = dict()
    for param in param_search:
        sql = "select DISTINCT %s from hos_list %s" % (param, str_search[:-5])
        cursor.execute(sql)
        data = cursor.fetchall()
        dict_data[param] = [i[0] for i in data]
    cursor.close()
    con_mysql_connect.close()
    return dict_data


def func_for_general_statistics_admin(start_time, end_time, param_dict=None):
    '''

    :param start_time: 起始时间
    :param end_time: 结束时间
    :return:
    '''
    dict_for_table = {}
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    sql_all = "select SUM(cost) FROM order_list where startTime > '%s' and startTime < '%s'" % \
              (start_time, end_time)
    cursor.execute(sql_all)
    data_all_profit = cursor.fetchone()  # 总收入
    sql_refund = "select SUM(withdrawMoney) FROM refund_payment where raiseTime > '%s' and raiseTime < '%s' " \
                 "and  status = '0'" % \
                 (start_time, end_time)
    cursor.execute(sql_refund)
    data_refund = cursor.fetchone()
    try:
        num = float(data_all_profit[0]) - float(data_refund[0])
    except KeyError as e:
        if data_all_profit[0] is not None:
            num = data_all_profit[0]
        elif data_refund[0] is not None:
            num = data_refund[0]
        else:
            num = 0

    dict_for_table['income'] = {
        'all': data_all_profit[0],
        'refund': data_refund[0],
        'expend': num
    }
    sql_user_all = "select count(*) from user_list"
    cursor.execute(sql_user_all)
    data_user_all = cursor.fetchone()  # 总人数

    sql_user_add = "select count(*) from user_list where registerTime > '%s' and " \
                   "registerTime < '%s'" % (start_time, end_time)
    cursor.execute(sql_user_add)
    data_user_add = cursor.fetchone()  # 增长用户
    sql_user_active = "SELECT COUNT(DISTINCT( userId)),count(*) FROM order_list where startTime > '%s' and " \
                      "startTime < '%s'" % (start_time, end_time)
    cursor.execute(sql_user_active)  # 活跃用户
    data_user_active = cursor.fetchone()
    dict_for_table['userStatus'] = {
        'all': data_user_all[0],
        'add': data_user_add[0],
        'active': data_user_active[0]
    }
    sql_count_all = "select count(*) from order_list"
    cursor.execute(sql_count_all)
    data_count_all = cursor.fetchone()  # 总使用次数
    sql_count_time = "select count(*) from order_list order_list where startTime > '%s' and " \
                     "startTime < '%s'" % (start_time, end_time)
    cursor.execute(sql_count_time)
    data_count_time = cursor.fetchone()  # 段时间使用次数
    dict_for_table['useCount'] = {
        'all': data_count_all[0],
        'time': data_count_time[0],
    }
    sql_device_all = 'select count(*) from device_compose'
    cursor.execute(sql_device_all)
    data_device_all = cursor.fetchone()
    sql_device_using = "select count(*) from order_list where endTime is Null"
    cursor.execute(sql_device_using)
    data_device_useing = cursor.fetchone()
    dict_for_table['device'] = {
        'all': data_device_all[0],
        'using': data_device_useing[0],
        'free': int(data_device_all[0]) - int(data_device_useing[0])
    }
    print('dict_for_table', dict_for_table)
    return dict_for_table


def func_for_general_statistics_manager(start_time, end_time, agentId):
    dict_for_table = {}
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    sql_all = "select SUM(cost) FROM order_list where startTime > '%s' and startTime < '%s' and agentId = '%s'" % \
              (start_time, end_time, agentId)
    cursor.execute(sql_all)
    data_all_profit = cursor.fetchone()  # 总收入
    sql_refund = "select SUM(withdrawMoney) FROM refund_payment where raiseTime > '%s' and raiseTime < '%s' " \
                 "and  status = '0' and agentId = '%s'" % \
                 (start_time, end_time, agentId)
    cursor.execute(sql_refund)
    data_refund = cursor.fetchone()
    try:
        num = float(data_all_profit[0]) - float(data_refund[0])
    except KeyError as e:
        if data_all_profit[0] is not None:
            num = data_all_profit[0]
        elif data_refund[0] is not None:
            num = data_refund[0]
        else:
            num = 0
    dict_for_table['income'] = {
        'all': data_all_profit[0],
        'refund': data_refund[0],
        'expend': num
    }
    sql_user_all = "select count(*) from user_list"
    cursor.execute(sql_user_all)
    data_user_all = cursor.fetchone()  # 总人数

    sql_user_add = "select count(*) from user_list where registerTime > '%s' and " \
                   "registerTime < '%s'" % (start_time, end_time)
    cursor.execute(sql_user_add)
    data_user_add = cursor.fetchone()  # 增长用户
    sql_user_active = "SELECT COUNT(DISTINCT( userId)),count(*) FROM order_list where startTime > '%s' and " \
                      "startTime < '%s' and agentId = '%s'" % (start_time, end_time, agentId)
    cursor.execute(sql_user_active)  # 活跃用户
    data_user_active = cursor.fetchone()
    dict_for_table['userStatus'] = {
        'all': data_user_all[0],
        'add': data_user_add[0],
        'active': data_user_active[0]
    }
    sql_count_all = "select count(*) from order_list where agentId = '%s'" % agentId
    cursor.execute(sql_count_all)
    data_count_all = cursor.fetchone()  # 总使用次数
    sql_count_time = "select count(*) from order_list order_list where startTime > '%s' and " \
                     "startTime < '%s' and agentId = '%s'" % (start_time, end_time, agentId)
    cursor.execute(sql_count_time)
    data_count_time = cursor.fetchone()  # 段时间使用次数
    dict_for_table['useCount'] = {
        'all': data_count_all[0],
        'time': data_count_time[0],
    }
    sql_device_all = "select count(*) from device_compose where agentId = '%s'" % agentId
    cursor.execute(sql_device_all)
    data_device_all = cursor.fetchone()
    sql_device_useing = "select count(*) from order_list where endTime is Null and agentId = '%s'" % agentId
    cursor.execute(sql_device_useing)
    data_device_useing = cursor.fetchone()
    dict_for_table['device'] = {
        'all': data_device_all[0],
        'using': data_device_useing[0],
        'free': int(data_device_all[0]) - int(data_device_useing[0])
    }
    return dict_for_table


def address_location(address):
    '''
    根据地址返回经纬度
    :param address: 地址
    :return: 经纬度
    '''
    geolocator = Baidu('EiQTTRKzlV3dKN1zcZ3c7iVhIl126xvC')
    location = geolocator.geocode(address)
    return {'latitude': location.latitude, 'longitude': location.longitude}


def search_total_data_by_terms(search_range_word, time_range=None, agentName=None):
    '''
    首页条形 统计查询
    :param search_range_word:
    :param search_range_time:
    :return:
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    search_word = " and "
    for k, v in search_range_word.items():
        if v is None or len(v) == 0:
            pass
        else:
            search_word += "order_list.`%s` = '%s' and " % (k, v)
    search_word = search_word[0:-4]

    if time_range is None:
        pass
    else:
        search_word += (' and ' + time_range)
    sql_1 = "SELECT SUM(order_list.`cost`), hos_list.`agentName`, hos_list.`hosRatio`,  hos_list.`agentRatio`,COUNT(1)," \
            " SUM(order_list.`cost`* (1-hos_list.`hosRatio`)*hos_list.`agentRatio`) FROM hos_list LEFT JOIN" \
            " order_list ON order_list.`deviceId` = hos_list.`deviceId` WHERE order_list.`cost`" \
            " IS NOT NULL %s GROUP BY order_list.`agentName`" % search_word  # 净利润 总收入
    cursor.execute(sql_1)
    data_1 = cursor.fetchall()
    if time_range is None:
        if agentName is None:
            refund_sql = None
        else:
            refund_sql = " where agentName = '%s'  GROUP BY agentName " % agentName
    else:
        if agentName is None:
            if search_range_word.get('agentName') is None or len(search_range_word.get('agentName')) == 0:
                refund_sql = "where " + time_range.replace("order_list.`startTime`",
                                                           "raiseTime") + ' GROUP BY agentName'
            else:
                refund_sql = "where " + time_range.replace("order_list.`startTime`", "raiseTime")
                refund_sql += " and agentName = '%s'  GROUP BY agentName" % search_range_word.get('agentName')
        else:
            refund_sql = "where " + time_range.replace("order_list.`startTime`", "raiseTime")
            refund_sql += " and agentName = '%s' GROUP BY agentName" % agentName
    sql_2 = "SELECT SUM(withdrawMoney), agentName FROM refund_payment %s   " % refund_sql  # 已退款
    cursor.execute(sql_2)
    data_2 = cursor.fetchall()
    if time_range is None or len(time_range) < 1:
        time_ = "'" + str((datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")) + "'"
    else:
        time_ = time_range.split('<')[-1]
    sql_3 = "SELECT COUNT(1) FROM user_list"
    sql_4 = "SELECT COUNT(userId) FROM order_list"
    sql_5 = "SELECT COUNT(1) FROM user_list WHERE registerTime > %s" % time_
    cursor.execute(sql_3)
    data_3 = cursor.fetchone()
    cursor.execute(sql_4)
    data_4 = cursor.fetchone()
    cursor.execute(sql_5)
    data_5 = cursor.fetchone()
    search_count_words = 'where '
    if agentName is None:
        if time_range is None:
            search_count_words = None
        else:
            search_count_words += time_range
    else:
        if time_range is None:
            search_count_words += "agentName = '%s'" % agentName
        else:
            search_count_words += "agentName = '%s' and %s " % (agentName, time_range)

    sql_6 = "SELECT COUNT(*) FROM order_list %s " % search_count_words
    sql_7 = "SELECT COUNT(*) FROM order_list"
    cursor.execute(sql_6)
    data_6 = cursor.fetchone()
    cursor.execute(sql_7)
    data_7 = cursor.fetchone()
    # 条件整合
    if agentName is None or len(agentName) <= 1:
        if search_range_word.get('agentName') is None:
            sql_8 = "SELECT COUNT(*) FROM device_compose"
            sql_9 = "SELECT COUNT(*) FROM order_list WHERE startTime IS NOT NULL AND endTime IS NULL "
        else:
            search_w = " where agentName = '%s'" % search_range_word.get('agentName')
            sql_8 = "SELECT COUNT(*) FROM device_compose %s" % search_w
            sql_9 = "SELECT COUNT(*) FROM order_list WHERE startTime IS NOT NULL AND endTime IS NULL and %s" % search_w
    else:
        search_w = " where agentName = '%s'" % agentName
        sql_8 = "SELECT COUNT(*) FROM device_compose %s" % search_w
        sql_9 = "SELECT COUNT(*) FROM order_list WHERE startTime IS NOT NULL AND endTime IS NULL AND %s" % search_w
    print(sql_9)
    cursor.execute(sql_8)
    data_8 = cursor.fetchone()
    cursor.execute(sql_9)
    data_9 = cursor.fetchone()

    cursor.close()
    con_mysql_connect.close()

    income = sum([i[0] for i in data_1])  # 总收入
    expend = sum([i[5] for i in data_1])  # 净利润
    refund = sum([i[0] for i in data_2])  # 已退款

    total_user = data_3[0]  # 总用户量
    active_user = data_4[0]  # 活跃用户
    growing_user = data_5[0]  # 新增用户

    use_counts = data_6[0]  # 使用次数
    total_counts = data_7[0]  # 使用总次数

    total_device = data_8[0]  # 设备总量
    using_device = data_9[0]  # 使用中设备
    free_device = int(total_device) - int(using_device)  # 空闲设备
    return {
        'income': income, 'expend': expend, 'refund': refund,
        'totalUser': total_user, 'activeUser': active_user,
        'useCounts': use_counts, 'totalCounts': total_counts,
        'totalDevice': total_device, 'usingDevice': using_device, 'freeDevice': free_device
    }


def search_data_for_device_status(user_info, search_words_input,
                                  start_time=None, end_time=None):
    if user_info[0] == '0':
        search_w = " where"
        for k, v in search_words_input.items():
            if v is None or len(v) < 1:
                pass
            else:
                search_w += " %s = '%s' and  " % (k, v)
        if None in [start_time, end_time]:
            sql_1_start_time = search_w[0: -5]
            sql_2_import_time = search_w[0: -5]
        else:
            if len(search_w) >= 5:
                sql_1_start_time = search_w + " and '%s' < startTime and startTime < '%s' " % (start_time, end_time)
                sql_2_import_time = search_w + " and '%s' < importTime  and importTime < '%s' " % (start_time, end_time)
            else:
                sql_1_start_time = "  '%s' < startTime  and startTime < '%s' " % (start_time, end_time)
                sql_2_import_time = "  '%s' < importTime and importTime < '%s' " % (start_time, end_time)
        sql_1 = "SELECT COUNT(1), SUM(cost),  SUBSTRING(startTime, 1, 10) FROM order_list AS o," \
                " hos_list AS d WHERE o.`deviceId` = d.`deviceId` %s GROUP BY SUBSTRING(startTime, 1, 10 ) " \
                "ORDER BY startTime DESC" % sql_1_start_time.replace('where', 'and')

        sql_2 = "SELECT COUNT(1), SUBSTRING(importTime, 1, 10) FROM maintain_repair AS o,  hos_list AS d" \
                " WHERE o.`deviceId` = d.`deviceId` %s  GROUP BY importTime " % sql_2_import_time.replace('where',
                                                                                                          'and')
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql_1)
        data_1 = cursor.fetchall()
        cursor.execute(sql_2)
        data_2 = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        dict_2 = {}
        for i in data_1:
            dict_2[i[2]] = {'count': i[0], 'cost': i[1], 'repairs': 0}
        for data in data_2:
            if data[1] in dict_2:
                dict_2[data[1]]["repair"] = 0 if data[0] is None else data[0]
            else:
                dict_2[data[1]] = {'count': 0, 'cost': 0, 'repairs': data[0]}
        return dict_2
    else:
        search_words_input.pop("d.`agentName`")
        search_w = " and "
        for k, v in search_words_input.items():
            if v is None or len(v) < 1:
                pass
            else:
                search_w += " %s = '%s' and  " % (k, v)
        if None in [start_time, end_time]:
            sql_1_start_time = search_w[0: -5]
            sql_2_import_time = search_w[0: -5]
        else:
            if len(search_w) >= 5:
                sql_1_start_time = search_w + " and '%s' < startTime and startTime < '%s' " % (start_time, end_time)
                sql_2_import_time = search_w + " and '%s' < importTime  and importTime < '%s' " % (start_time, end_time)
            else:
                sql_1_start_time = "  '%s' < startTime  and startTime < '%s' " % (start_time, end_time)
                sql_2_import_time = "  '%s' < importTime and importTime < '%s' " % (start_time, end_time)
        agent_name = user_info[2]
        sql_1 = "SELECT COUNT(1), SUM(cost),  SUBSTRING(startTime, 1, 10) FROM order_list AS o, hos_list AS d" \
                " WHERE o.`deviceId` = d.`deviceId` and d.`agentName` = '%s' %s " \
                "GROUP BY SUBSTRING(startTime, 1, 10 ) ORDER BY startTime DESC" % (agent_name, sql_1_start_time)

        sql_2 = "SELECT COUNT(1), SUBSTRING(importTime, 1, 10) FROM maintain_repair AS o,  hos_list" \
                " AS d WHERE o.`deviceId` = d.`deviceId` and d.`agentName` = '%s' %s  order BY importTime " % (
                    agent_name, sql_2_import_time)
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql_1)
        data_1 = cursor.fetchall()
        cursor.execute(sql_2)
        data_2 = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        dict_2 = {}
        for i in data_1:
            dict_2[i[2]] = {'count': i[0], 'cost': i[1], 'repairs': 0}
        for data in data_2:
            if data[1] in dict_2:
                dict_2[data[1]]["repair"] = 0 if data[0] is None else data[0]
            else:
                dict_2[data[1]] = {'count': 0, 'cost': 0, 'repairs': data[0]}
        return dict_2


def map_data(sql_1, sql_2, sql_3):
    '''

    :param data_1: 查询结果
    :param data_2: 同上
    :param data_3: 同上
    :return:
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql_1)
    data_1 = cursor.fetchall()
    cursor.execute(sql_2)
    data_2 = cursor.fetchall()
    cursor.execute(sql_3)
    data_3 = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    dict_data = dict()
    for data in data_1:
        dict_data[data[2] + data[3]] = {'useCount': 0 if data[0] is None else data[0],
                                        'totalIncome': 0 if data[1] is None else data[1],
                                        'deviceNum': 0, 'hosNum': 0, 'repairsCount': 0}
    for d2 in data_2:
        if d2[2] + d2[3] in dict_data.keys():
            dict_data[d2[2] + d2[3]]['deviceNum'] = 0 if d2[0] is None else d2[0]
            dict_data[d2[2] + d2[3]]['hosNum'] = 0 if d2[1] is None else d2[1]
        else:
            dict_data[d2[2] + d2[3]] = {'useCount': 0, 'totalIncome': 0,
                                        'deviceNum': 0 if d2[0] is None else d2[0],
                                        'hosNum': 0 if d2[1] is None else d2[1],
                                        'repairsCount': 0}
    for d3 in data_3:
        if d3[1] + d3[2] in dict_data.keys():
            location_data = address_location(address=d3[1] + d3[2])
            dict_data[d3[1] + d3[2]]['deviceNum'] = 0 if d3[0] is None else d3[0]
            dict_data[d3[1] + d3[2]]['latitude'] = location_data.get('latitude')
            dict_data[d3[1] + d3[2]]['longitude'] = location_data.get('longitude')
        else:
            location_data = address_location(address=d3[1] + d3[2])
            dict_data[d3[1] + d3[2]] = {'useCount': 0, 'totalIncome': 0,
                                        'deviceNum': 0,
                                        'hosNum': 0,
                                        'repairsCount': 0 if d3[0] is None else d3[0],
                                        'latitude': location_data.get('latitude'),
                                        'longitude': location_data.get('longitude')}
    return dict_data


def table_data_by_sql(sql_1, sql_2, sql_3):
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql_1)
    data_1 = cursor.fetchall()
    cursor.execute(sql_2)
    data_2 = cursor.fetchall()
    cursor.execute(sql_3)
    data_3 = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    return_dict = dict()
    for d1 in data_1:
        return_dict[d1[2]] = {
            'deviceNum': d1[0] if d1[0] is not None else 0,
            'hosNum': d1[1] if d1[1] is not None else 0,
            'orderNum': 0,
            'repairs': 0,
        }
    for d2 in data_2:
        if d2[1] in return_dict.keys():
            return_dict[d2[1]]['orderNum'] = d2[0] if d2[0] is not None else 0
        else:
            return_dict[d2[1]] = {
                'deviceNum': 0,
                'hosNum': 0,
                'orderNum': d2[0] if d2[0] is not None else 0,
                'repairs': 0,
            }
    for d3 in data_3:
        if d3[1] in return_dict.keys():
            return_dict[d3[1]]['repairs'] = d3[0] if d3[0] is not None else 0
        else:
            return_dict[d3[1]] = {
                'deviceNum': 0,
                'hosNum': 0,
                'orderNum': 0,
                'repairs': d3[0] if d3[0] is not None else 0,
            }
    return return_dict


def func_for_get_search(sql_1, sql_2):
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql_1)
    data_1 = cursor.fetchall()
    cursor.execute(sql_2)
    data_2 = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    print(data_1)
    print(data_2)
    return_dict = dict()
    for d1 in data_1:
        return_dict[d1[4]] = {
            'orderNum': d1[0] if d1[0] is not None else 0,
            'allIncome': d1[1] if d1[1] is not None else 0,
            'hosNum': d1[2] if d1[2] is not None else 0,
            'userNum': d1[3] if d1[3] is not None else 0,
            'repair': 0,
        }
    for d2 in data_2:
        if d2[1] in return_dict.keys():
            return_dict[d2[1]]['repair'] = d2[0] if d2[0] is not None else 0
        else:
            return_dict[d2[1]] = {
                'orderNum': 0,
                'allIncome': 0,
                'hosNum': 0,
                'userNum': 0,
                'repair': d2[0] if d2[0] is not None else 0,
            }
    return return_dict


