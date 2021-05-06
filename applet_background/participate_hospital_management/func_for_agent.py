from applet_background.link_config import con_mysql


def check_user_auth_level(user_phone):
    '''

    :param user_phone:  用户手机号
    :return: 用户等级，代理商等信息
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute("select level, agentId, agentName from manager_list where phoneNumber = %s", user_phone)
    level = cursor.fetchone()
    cursor.close()
    con_mysql_connect.close()
    return level


def search_for_agent_data_list(dict_search=None):
    '''
    搜索 代理商信息
    :param dict_search:
    :return:
    '''
    search_str = str()
    sql = "SELECT agentId, agentName, ratio, account, agentPhone, joinTime FROM agent_list"
    if dict_search is None:
        sql = "SELECT agentId, agentName, ratio, account, agentPhone, joinTime FROM agent_list"
    else:
        for k, v in dict_search.items():
            if v is None or len(v) == 0:
                pass
            else:
                str_ = "%s = '%s' and " % (k, v)
                search_str += str_
    if search_str is not None and len(search_str) != 0:
        search_str = 'where ' + search_str[0:-4]
        sql = "SELECT agentId, agentName, ratio, account, agentPhone, joinTime FROM agent_list where %s" % search_str
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    list_return = list()
    for agent_info in data:
        dict_ = {
            'agentId': agent_info[0],
            'agentName': agent_info[1],
            'ratio': agent_info[2],
            'account': agent_info[3],
            'agentPhone': agent_info[4],
            'joinTime': agent_info[5]
        }
        list_return.append(dict_)
    return list_return


def withdrawal_order_list(user_info):
    if user_info[0] == '0':
        sql = ''
    else:
        agentId = user_info[1]  #
