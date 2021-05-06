from applet_background.link_config import con_mysql


def check_user_auth_level(user_phone):
    '''

    :param user_phone:  用户手机号
    :return: 用户等级，代理商等信息
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute("select level, agentId, agentName from manager_list where phoneNumber = %s", user_phone)
    user_info = cursor.fetchone()
    cursor.close()
    con_mysql_connect.close()
    return user_info


def search_user_list_data(page_number=1, page_size=10, search_dict=None):
    '''

    :param user_info:
    :param page_numbe:
    :param page_size:
    :param search_dict:
    :return:
    '''
    search_param = str()
    if search_dict is None:
        pass
    else:
        for k, v in search_dict.items():
            if v is None or len(v) == 0:
                pass
            else:
                if k != 'deposit':
                    str_ = "%s = '%s' and " % (k, v)
                    search_param += str_
                else:
                    str_ = "%s is '%s' and " % (k, v)
                    search_param += str_

    if search_param is not None and len(search_param) != 0:
        search_str = 'where ' + search_param[0:-4]
    else:
        search_str = ''

    sql = "SELECT userId,userName, headUrl,phoneNumber, deposit, registerTime FROM user_list %s limit %s,%s" % \
          (search_str, int(page_size) * (int(page_number) - 1), int(page_size) * int(page_number))
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    sql_count = "select count(*) from user_list"
    cursor.execute(sql_count)
    count = cursor.fetchone()
    cursor.close()
    con_mysql_connect.close()
    list_return = list()
    for user_info in data:
        status = '未交' if user_info[4] is None else '已交'
        dict_ = {
            'userId': user_info[0],
            'userName': user_info[1],
            'headUrl': user_info[2],
            'phoneNumber': user_info[3],
            'deposit': user_info[4],
            'registerTime': user_info[5],
            'depositType': status
        }
        list_return.append(dict_)
    return {'count': count[0], 'userList': list_return}

