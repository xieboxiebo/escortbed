
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


def search_hospital_data(user_info, search_dict=None):
    '''
    医院列表数据
    :param user_info: 用户信息
    :param search_dict: 筛选条件
    :return: 查询结果
    '''
    if user_info[0] == '0':
        '''
        平台管理员
        '''
        if search_dict is None:
            sql = "SELECT hos_list.hosName, hos_list.`province`, hos_list.`city`, hos_list.`area`, hos_list.`addr`, " \
                  "hos_list.`agentName`, hos_list.`modeId`,hos_list.`modeName`, hos_list.`hosRatio`, " \
                  "COUNT(hos_list.`deviceId`)," \
                  "agent_list.`agentPhone` FROM hos_list JOIN agent_list " \
                  " WHERE hos_list.`agentId` = agent_list.`agentId`" \
                  " GROUP BY hos_list.`hosName`  "
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            con_mysql_connect.close()
            hos_data_list = list()
            for hos_data in data:
                hos_data_list.append({
                    'hosName': hos_data[0],
                    'hosProvince': hos_data[1],
                    'hosCity': hos_data[2],
                    'hosArea': hos_data[3],
                    'hosAddr': hos_data[4],
                    'agentName': hos_data[5],
                    'modeId': hos_data[6],
                    'modeName': hos_data[7],
                    'ratio': hos_data[8],
                    'count': hos_data[9],
                    'agentPhone': hos_data[10]
                })
            return hos_data_list
        else:
            str_search = 'and '
            for k, v in search_dict.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    if k in ['hosName', 'agentName', 'modeName']:
                        str_ = " hos_list.`%s` = '%s' and " % (k, v)
                    else:
                        str_ = " agent_list.`agentPhone` = '%s'  and " % v
                    str_search += str_

            sql = "SELECT hos_list.hosName, hos_list.`province`, hos_list.`city`, hos_list.`area`, hos_list.`addr`, " \
                  "hos_list.`agentName`, hos_list.`modeId`,hos_list.`modeName`, hos_list.`hosRatio`, " \
                  "COUNT(hos_list.`deviceId`)," \
                  "agent_list.`agentPhone` FROM hos_list JOIN agent_list " \
                  " WHERE hos_list.`agentId` = agent_list.`agentId`  %s" \
                  " GROUP BY hos_list.`hosName`  " % str_search[0:-4]
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            con_mysql_connect.close()
            hos_data_list = list()
            for hos_data in data:
                hos_data_list.append({
                    'hosName': hos_data[0],
                    'hosProvince': hos_data[1],
                    'hosCity': hos_data[2],
                    'hosArea': hos_data[3],
                    'hosAddr': hos_data[4],
                    'agentName': hos_data[5],
                    'modeId': hos_data[6],
                    'modeName': hos_data[7],
                    'ratio': hos_data[8],
                    'count': hos_data[9],
                    'agentPhone': hos_data[10]
                })
            return hos_data_list
    else:
        '''
        一般管理员
        '''
        if search_dict is None:
            sql = "SELECT hos_list.hosName, hos_list.`province`, hos_list.`city`, hos_list.`area`, hos_list.`addr`, " \
                  "hos_list.`agentName`, hos_list.`modeId`,hos_list.`modeName`, hos_list.`hosRatio`, " \
                  "COUNT(hos_list.`deviceId`)," \
                  "agent_list.`agentPhone` FROM hos_list JOIN agent_list " \
                  " WHERE hos_list.`agentId` = agent_list.`agentId` and hos_list.`agentId` = '%s'" \
                  " GROUP BY hos_list.`hosName`  " % user_info[1]
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            con_mysql_connect.close()
            hos_data_list = list()
            for hos_data in data:
                hos_data_list.append({
                    'hosName': hos_data[0],
                    'hosProvince': hos_data[1],
                    'hosCity': hos_data[2],
                    'hosArea': hos_data[3],
                    'hosAddr': hos_data[4],
                    'agentName': hos_data[5],
                    'modeId': hos_data[6],
                    'modeName': hos_data[7],
                    'ratio': hos_data[8],
                    'count': hos_data[9],
                    'agentPhone': hos_data[10]
                })
            return hos_data_list
        else:
            str_search = 'and '
            for k, v in search_dict.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    if k in ['hosName', 'agentName', 'modeName']:
                        str_ = " hos_list.`%s` = '%s' and " % (k, v)
                    else:
                        str_ = " agent_list.`agentPhone` = '%s'  and " % v
                    str_search += str_

            sql = "SELECT hos_list.hosName, hos_list.`province`, hos_list.`city`, hos_list.`area`, hos_list.`addr`, " \
                  "hos_list.`agentName`, hos_list.`modeId`,hos_list.`modeName`, hos_list.`hosRatio`, " \
                  "COUNT(hos_list.`deviceId`)," \
                  "agent_list.`agentPhone` FROM hos_list JOIN agent_list " \
                  " WHERE hos_list.`agentId` = agent_list.`agentId` and hos_list.`agentId` = '%s'  %s" \
                  " GROUP BY hos_list.`hosName`  " % (user_info[1], str_search[0:-4])
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            con_mysql_connect.close()
            hos_data_list = list()
            for hos_data in data:
                hos_data_list.append({
                    'hosName': hos_data[0],
                    'hosProvince': hos_data[1],
                    'hosCity': hos_data[2],
                    'hosArea': hos_data[3],
                    'hosAddr': hos_data[4],
                    'agentName': hos_data[5],
                    'modeId': hos_data[6],
                    'modeName': hos_data[7],
                    'ratio': hos_data[8],
                    'count': hos_data[9],
                    'agentPhone': hos_data[10]
                })
            return hos_data_list


def search_hospital_department_data(user_info, search_dict):
    if user_info[0] == '0':
        str_search = 'where'
        for k, v in search_dict.items():
            if v is None or len(v) == 0:
                pass
            else:
                str_ = " %s = '%s' and " % (k, v)
                str_search += str_
        sql = "SELECT hosName, agentName, hosDepartM ,addr," \
              " COUNT(deviceId) FROM hos_list %s GROUP BY hosDepartM, hosName" \
              % str_search[0: -4]
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        department_list = list()
        for department in data:
            department_list.append({
                'hosName': department[0],
                'agentName': department[1],
                'department': department[2],
                'addr': department[3],
                'count': department[4]
            })
        return department_list
    else:
        str_search = 'and '
        for k, v in search_dict.items():
            if v is None or len(v) == 0:
                pass
            else:
                str_ = " %s = '%s' and " % (k, v)
                str_search += str_
        sql = "SELECT hosName, agentName, hosDepartM ,addr," \
              " COUNT(deviceId) FROM hos_list where agentId = '%s' %s GROUP BY hosDepartM, hosName" \
              % (user_info[1], str_search[0: -4])
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        department_list = list()
        for department in data:
            department_list.append({
                'hosName': department[0],
                'agentName': department[1],
                'department': department[2],
                'addr': department[3],
                'count': department[4]
            })
        return department_list

