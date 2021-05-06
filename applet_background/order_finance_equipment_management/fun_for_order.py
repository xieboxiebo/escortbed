from applet_background.link_config import con_mysql


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


def get_order_deposit_data_by_sql(sql):
    '''
    通过sql语句查询押金列表
    :param sql:
    :return:
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    return_list = list()
    for data_ in data:
        return_list.append(
            {
                'orderId': data_[0],
                'hoaName': data_[1],
                'userName': data_[2],
                'phoneNumber': data_[3],
                'money': data_[4],
                'agentName': data_[5],
                'createTime': data_[6],
                'status': data_[7],
            }
        )
    return return_list


def get_order_data_by_sql(sql):
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    return_list = list()
    for order_data in data:
        return_list.append({
            'orderNum': order_data[0],
            'userName': order_data[0],
            'phoneNumber': order_data[0],
            'deviceId': order_data[0],
            'hosName': order_data[0],
            'agentName': order_data[0],
            'startTime': order_data[0],
            'endTime': order_data[0],
            'cost': order_data[0],
            'couponId': order_data[0],
            'orderStatus': order_data[0],
        })
    return return_list


sql = "SELECT orderNum, userName, phoneNumber, order_list.`deviceId`, hos_list.`hosName`, " \
      "order_list.`agentName`, startTime, endTime,cost,couponId, orderStatus FROM order_list, " \
      "hos_list WHERE order_list.`deviceId` = hos_list.`deviceId`"
get_order_data_by_sql(sql)
