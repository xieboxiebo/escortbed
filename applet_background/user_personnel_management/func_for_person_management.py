import random
import string
import time

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
    print('level', level)
    return level


def manager_list_get(user_info):
    '''

    :param user_info:
    :return:
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    if user_info[0] == '0':
        sql = "SELECT managerId, managerName,agentName, roleName, phoneNumber, loginTime FROM manager_list limit 10"
    else:
        sql = " SELECT managerId, managerName,agentName, roleName, phoneNumber, loginTime FROM manager_list where " \
              "agentName = '%s' limit 10" % user_info[2]
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    list_for_return = list()
    for manager_info in data:
        dict_manager = {
            'managerId': manager_info[0],
            'managerName': manager_info[1],
            'agentName': manager_info[2],
            'roleName': manager_info[3],
            'phoneNumber': manager_info[4],
            'loginTime': manager_info[5]
        }
        list_for_return.append(dict_manager)
    return list_for_return


def manager_list_data_for_search(dict_search, pageSize, pageNumber):
    '''

    :param dict_search: 查询条件
    :param pageSize: 每页展示的数据量
    :param pageNumber: 页数
    :return: 查询的结果
    '''
    search_str = str()
    for k, v in dict_search.items():
        if v is None:
            pass
        else:
            str_ = "%s = '%s' and " % (k, v)
            search_str += str_
    if len(search_str) != 0:
        search_str = 'where ' + search_str[0:-4]
        sql = " SELECT managerId, managerName,agentName, roleName, phoneNumber, loginTime FROM manager_list %s " \
              "limit %s, %s" % (search_str, int(pageSize) * (int(pageNumber) - 1), int(pageSize) * int(pageNumber))
    else:
        sql = " SELECT managerId, managerName,agentName, roleName, phoneNumber, loginTime FROM manager_list " \
              "limit %s,%s" % (int(pageSize) * (int(pageNumber) - 1), int(pageSize) * int(pageNumber))
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    list_for_return = list()
    for manager_info in data:
        dict_manager = {
            'managerId': manager_info[0],
            'managerName': manager_info[1],
            'agentName': manager_info[2],
            'roleName': manager_info[3],
            'phoneNumber': manager_info[4],
            'loginTime': manager_info[5]
        }
        list_for_return.append(dict_manager)
    return list_for_return


def drop_list_data(user_info):
    '''
    下拉数据
    :param user_info: 用户信息
    :return:
    '''
    if user_info[0] == '0':
        sql_managerName = "SELECT DISTINCT managerName  FROM manager_list"
        sql_agentName = "SELECT DISTINCT agentName  FROM manager_list"
        sql_role = "SELECT roleName FROM role_table "
    else:
        sql_managerName = "SELECT DISTINCT managerName FROM manager_list where agentName = '%s'" % \
                          user_info[2]
        sql_agentName = "SELECT DISTINCT agentName  FROM manager_list where agentName = '%s'" % user_info[2]
        sql_role = "SELECT roleName FROM role_table where roleName != '超级管理员'"
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute(sql_managerName)  # 管理员名字
    manager_list = cursor.fetchall()
    cursor.execute(sql_agentName)  # 管理员名字
    agent_list = cursor.fetchall()
    cursor.execute(sql_role)
    role_list = cursor.fetchall()
    cursor.close()
    con_mysql_connect.close()
    return {'managerList': [i[0] for i in manager_list],
            'agentList': [i[0] for i in agent_list],
            'roleName': [i[0] for i in role_list]}


def add_manager_data(managerName, managerPhone, passWord, agentName, roleName, email):
    '''
    新增管理员接口
    :param managerName:  名称
    :param managerPhone: 手机号
    :param passWord: 密码
    :param agentName: 代理商名称
    :param roleName: 角色名称
    :param email: 邮件
    :return:
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute("select agentId, level from agent_list where agentName = '%s'", agentName)
    agent_data = cursor.fetchone()
    agentId = agent_data[0]
    level = agent_data[1]
    cursor.execute("select roleId from role_table where roleName = '%s'", roleName)
    role_data = cursor.fetchone()
    roleId = role_data[0]
    managerId = str(time.time())[2:13].replace('.', random.choice(string.ascii_letters))
    sql_insert = "insert into manager_list (managerId, managerName, phoneNumber,passWord, agentId" \
                 "agentName, roleName, roleId,email, level ) values ('%s', '%s','%s', '%s','%s', '%s','%s'," \
                 " '%s','%s','%s')" \
                 % (managerId, managerName, managerPhone, passWord, agentId, agentName, roleName, roleId, email, level)
    cursor.execute(sql_insert)
    cursor.close()
    con_mysql_connect.close()
    return True


def phone_number_manager_name_exit(managerName, phoneNumber):
    '''
    判断用户名或者手机号是否已存在在系统中
    :param managerName:
    :param phoneNumber:
    :return:
    '''
    con_mysql_connect = con_mysql.connection()
    cursor = con_mysql_connect.cursor()
    cursor.execute("select 1 from manager_list where managerName='%s' or phoneNumber = '%s'"
                   " limit 1", managerName, phoneNumber)
    count = cursor.fetchone()
    cursor.close()
    con_mysql_connect.close()
    if str(count[0]) == '0':
        return True
    else:
        return False
