'''
time: 2020.8.19
author: ljx
model: system homepage
other: CBV
'''
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views import View

from applet_background.link_config import con_mysql
from applet_background.system_config import str_to_token
from system_home.func_for_system_views import check_login_authentication, drop_down_list_data, drop_down_list_by_param, \
    check_user_auth_level, func_for_general_statistics_admin, func_for_general_statistics_manager, \
    search_total_data_by_terms, search_data_for_device_status, map_data, table_data_by_sql, func_for_get_search


class BackgroundLogin(View):
    '''
    后台登录接口
    '''

    def post(self, request):

        '''
        :param request:
        :param phoneNum:  管理员手机号
        :param passWord:  管理员密码
        :return: 登录结果
        '''
        phone_number = request.POST.get('phoneNum', None)
        pass_word = request.POST.get('passWord', None)
        print(phone_number, pass_word)
        if None in [pass_word, phone_number]:
            return JsonResponse({'code': 500, 'msg': '参数不全', 'level': None})
        if check_login_authentication(user_phone=phone_number, pass_word=pass_word):
            level = check_user_auth_level(user_phone=phone_number)[0]  # 用户等级 ，函数返回level, agentId, agentName
            token_ = str_to_token(key=phone_number)  # token加密
            response = JsonResponse({'code': 200, 'msg': '登录成功', 'level': level})
            response.set_cookie('ph', phone_number, max_age=60 * 60 * 24 * 15)  # 手机号码存入cook
            response.set_cookie('tk', token_, max_age=60 * 60 * 24 * 15)  # token化的手机号码存入cook
            return response
        else:
            return JsonResponse({'code': 500, 'msg': '密码或用户名不正确！'})


class GeneralStatistics(View):
    '''
    后台首页统计表 代理商利润 使用次数 设备状态 用户总量等
    '''

    def get(self, request):
        '''
        :param request:
        :return:
        '''
        phone = request.COOKIES.get('ph')  # 获取手机号
        now_time = datetime.now()  # 当前时间
        before_time = datetime.now() - timedelta(days=7)  # 七天前时间
        user_info = check_user_auth_level(user_phone=phone)  # level, agentId, agentName
        if user_info[0] == '0':
            '''
            超级管理员
            '''
            data = func_for_general_statistics_admin(start_time=before_time, end_time=now_time)
            return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})
        else:
            '''
            代理商
            '''

            data = func_for_general_statistics_manager(start_time=before_time, end_time=now_time, agentId=user_info[1])
            return JsonResponse({'data': data, 'code': 200, 'msg': '后台统计表/table'})

    def post(self, request):
        '''

        :param request:
        :return:
        '''
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(phone)

        end_time = request.POST.get('endTime', None)  # 最近时间
        start_time = request.POST.get('oldTime', None)  # 最远时间

        agent_name = request.POST.get('agentName', None)  # 代理商姓名
        hos_name = request.POST.get('hosName', None)  # 医院名称
        department_name = request.POST.get('department', None)  # 科室名称

        province = request.POST.get('province', None)  # 省份
        city = request.POST.get('city', None)  # 城市
        area = request.POST.get('area', None)  # 地区
        time_range = None
        if None not in [start_time, end_time]:
            time_range = " and %s <= order_list.`startTime` < %s" % (start_time, end_time)
        search_range_word = {
            'agentName': agent_name,
            'hosName': hos_name,
            'departmentName': department_name,
            'province': province,
            'city': city,
            'area': area,
        }
        if user_info[0] == '0':
            '''
            平台管理员
            '''
            data = search_total_data_by_terms(search_range_word, time_range=time_range, agentName=None)
        else:
            '''
            代理商管理员
            '''
            data = search_total_data_by_terms(search_range_word, time_range=time_range, agentName=user_info[2])
        return JsonResponse({'data': data, 'code': 200, 'msg': '后台统计表/table'})


class ConsumptionState(View):
    '''
    消费订单统计图 echars
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            ''''
            平台管理员
            '''
            sql = "SELECT COUNT(1), SUM(cost),  SUBSTRING(startTime, 1, 10) FROM order_list" \
                  " GROUP BY SUBSTRING(startTime, 1, 10 ) ORDER BY startTime DESC LIMIT 7"
        else:
            agentName = user_info[2]
            sql = "SELECT COUNT(1), SUM(cost),  SUBSTRING(startTime, 1, 10) FROM order_list WHERE" \
                  " agentName = '%s' GROUP BY SUBSTRING(startTime, 1, 10 ) ORDER BY startTime DESC LIMIT 7" % agentName
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        return_data = list()
        for data_ in data:
            return_data.append(
                {
                    'time': data_[2],  # 时间
                    'count': data_[0],  # 使用次数
                    'cost': data_[1]  # 消费金额
                }
            )
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        end_time = request.POST.get('endTime', None)  # 最近时间
        start_time = request.POST.get('oldTime', None)  # 最远时间

        agent_name = request.POST.get('agentName', None)  # 代理商姓名
        hos_name = request.POST.get('hosName', None)  # 医院名称
        department_name = request.POST.get('department', None)  # 科室名称

        province = request.POST.get('province', None)  # 省份
        city = request.POST.get('city', None)  # 城市
        area = request.POST.get('area', None)  # 地区

        search_words = {
            'o.`agentName`': agent_name,
            'd.`hosName`': hos_name,
            'd.`hosDepartM`': department_name,
            'd.`province`': province,
            'd.`city`': city,
            'd.`area`': area
        }
        if None in [start_time, end_time]:
            search_time = None
        else:
            search_time = "and '%s' < o.`startTime` < '%s' " % (start_time, end_time)
        if user_info[0] == '0':
            ''''
            平台管理员
            '''
            search_w = 'and '
            for k, v in search_words.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    search_w += " %s = '%s' and  " % (k, v)
            sql = "SELECT COUNT(1), SUM(cost),  SUBSTRING(startTime, 1, 10) FROM order_list AS o, hos_list AS d" \
                  " WHERE o.`deviceId` = d.`deviceId` %s %s GROUP BY SUBSTRING(startTime, 1, 10 ) ORDER BY startTime DESC" \
                  % (search_w[0: -4], search_time)
        else:
            search_words["o.`agentName`"] = None
            agentName = user_info[2]
            search_w = 'and '
            for k, v in search_words.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    search_w += " %s = '%s' and " % (k, v)
            sql = "SELECT COUNT(1), SUM(cost),  SUBSTRING(startTime, 1, 10) FROM order_list WHERE" \
                  " agentName = '%s' %s %s GROUP BY SUBSTRING(startTime, 1, 10 ) ORDER BY startTime DESC LIMIT 7" % \
                  (agentName, search_w[0:-4], search_time)
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        return_data = list()
        for data_ in data:
            return_data.append(
                {
                    'time': data_[2],  # 时间
                    'count': 0 if data_[0] is None else data_[1],  # 使用次数
                    'cost': 0 if data_[1] is None else data_[1]  # 消费金额
                }
            )
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})


class EquipmentState(View):
    '''
    设备状态统计图
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql_1 = "SELECT COUNT(1), SUM(cost), SUBSTRING(startTime, 1, 10) " \
                    "FROM order_list GROUP BY SUBSTRING(startTime, 1, 10) ORDER BY startTime ASC"
            sql_2 = "SELECT COUNT(1), SUBSTRING(importTime, 1, 10) FROM maintain_repair " \
                    "GROUP BY SUBSTRING(importTime, 1, 10) ORDER BY importTime ASC "
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
            return JsonResponse({'data': dict_2, 'code': 200, 'msg': '请求成功！'})
        else:
            agent_name = user_info[2]
            sql_1 = "SELECT COUNT(1), SUM(cost), SUBSTRING(startTime, 1, 10) " \
                    "FROM order_list where agentName = '%s' GROUP BY SUBSTRING(startTime, 1, 10)" \
                    " ORDER BY startTime ASC limit 15" % agent_name
            sql_2 = "SELECT COUNT(1), SUBSTRING(importTime, 1, 10) FROM maintain_repair where agentName = '%s'" \
                    "GROUP BY SUBSTRING(importTime, 1, 10) ORDER BY importTime ASC limit 15" % agent_name
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
            return JsonResponse({'data': dict_2, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)

        start_time = request.POST.get('startTime', None)
        end_time = request.POST.get('endTime', None)

        agent_name = request.POST.get('agentName', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)
        hos_name = request.POST.get('hosName', None)
        hos_department = request.POST.get('hosDepartment', None)
        search_words_input = {
            "d.`agentName`": agent_name,
            "d.`province`": province,
            "d.`city`": city,
            "d.`area`": area,
            "d.`hoaName`": hos_name,
            "d.`hosDepartM`": hos_department,
        }
        data = search_data_for_device_status(user_info=user_info,
                                             search_words_input=search_words_input,
                                             start_time=start_time,
                                             end_time=end_time)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！   '})


class AgentListDataOverview(View):
    '''
    各个代理商数据概览
    '''

    def get(self, request):
        pass

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(phone)
        if user_info[0] == '0':
            sql = "SELECT SUM(order_list.`cost`), hos_list.`agentName`, COUNT(1), " \
                  "SUM(order_list.`cost`* (1-hos_list.`hosRatio`)*hos_list.`agentRatio`)," \
                  "COUNT(hos_list.`deviceId`) FROM hos_list LEFT JOIN order_list" \
                  " ON order_list.`deviceId` = hos_list.`deviceId`  GROUP BY order_list.`agentName`"
        else:
            sql = "SELECT SUM(order_list.`cost`), hos_list.`agentName`, COUNT(1), " \
                  "SUM(order_list.`cost`* (1-hos_list.`hosRatio`)*hos_list.`agentRatio`)," \
                  "COUNT(hos_list.`deviceId`) FROM hos_list LEFT JOIN order_list" \
                  " ON order_list.`deviceId` = hos_list.`deviceId` where order_list.`agentName` =" \
                  " '%s'   GROUP BY order_list.`agentName`" % user_info[2]
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        return_data = list()
        for data_ in data:
            return_data.append(
                {
                    'allCost': 0 if data_[0] is None else data_[0],
                    'agentName': data_[1],
                    'orderNum': 0 if data_[0] is None else data_[2],
                    'cost': 0 if data_[0] is None else data_[3],
                    'devices': 0 if data_[0] is None else data_[3],
                }
            )
        return JsonResponse({'data': return_data, 'code': 200, 'msg': '代理商信息概要滚动窗，请求成功！'})


class DropDownList(View):
    '''
    代理商信息概览 下拉列表数据 联动
    '''

    def get(self, request):
        try:
            phone = request.COOKIES.get('ph')  # 获取手机号
            data = drop_down_list_data(user_phone=phone)
            return JsonResponse({'data': data, 'code': 200, 'msg': 'get请求下拉列表数据，请求成功！处理不了给爸爸说！给你改'})
        except KeyError:
            return JsonResponse({'data': None, 'code': 500, 'msg': 'get请求下拉列表数据,请求失败！'})

    def post(self, request):
        '''
        不定参查询
        :param request:
        :return:
        '''
        agent_name = request.POST.get('agentName', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)
        hos_id = request.POST.get('hosId', None)
        hos_depart_m = request.POST.get('hosDepartM', None)
        param_dict = {'agentName': agent_name, 'province': province, 'city': city, 'area': area, 'hosId': hos_id,
                      'hosDepartM': hos_depart_m}
        data = drop_down_list_by_param(param_dict=param_dict)
        return JsonResponse({'data': data, 'code': 200, 'msg': 'post请求下拉列表数据，请求成功！处理不了给爸爸说！给你改'})


class OperationalMapDataList(View):
    '''
    代理商信息概览 地图
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql_1 = "SELECT COUNT(1), SUM(cost), city, AREA FROM order_list AS o, hos_list AS d " \
                    "WHERE o.`deviceId` = d.`deviceId` GROUP BY d.`area` "

            sql_2 = "SELECT COUNT(deviceId), COUNT(DISTINCT hosName), city, AREA FROM hos_list GROUP BY AREA"

            sql_3 = "SELECT COUNT(importTime), city, AREA FROM maintain_repair AS o, " \
                    "hos_list AS d WHERE o.`deviceId` = d.`deviceId` GROUP BY d.`area`"
        else:
            sql_1 = "SELECT COUNT(1), SUM(cost), city, AREA FROM order_list AS o, hos_list AS d " \
                    "WHERE o.`deviceId` = d.`deviceId` AND d.`agentName` = '%s' GROUP BY d.`area` " % user_info[2]

            sql_2 = "SELECT COUNT(deviceId), COUNT(DISTINCT hosName), city, AREA FROM hos_list WHERE agentName = '%s'" \
                    " GROUP BY AREA" % user_info[2]

            sql_3 = "SELECT COUNT(importTime), city, AREA FROM maintain_repair AS o, " \
                    "hos_list AS d WHERE o.`deviceId` = d.`deviceId` AND d.`agentName` = '%s' GROUP BY d.`area`" % \
                    user_info[2]
        data = map_data(sql_1, sql_2, sql_3)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        '''

        :param request:
        :return:
        '''
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        agent_name = request.POST.get('agentName', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)

        start_time = request.POST.get('startTime', None)
        end_time = request.POST.get('endTime', None)

        if user_info[0] == '0':
            param_search = {
                'd.`agentName`': agent_name,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_w = " and "
            for k, v in param_search.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_w += " %s = '%s'  and "
            param_search_ = {
                'd.`agentName`': agent_name,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_h = " and "
            for k, v in param_search_.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_h += " %s = '%s'  and "
            if None in [start_time, end_time]:
                time_range_order = None
                time_range_repair = None
                time_range_hos = 'where '
            else:
                time_range_order = " and '%s' < o.`startTime` and o.`startTime` < '%s' " % (start_time, end_time)
                time_range_repair = " and '%s' < o.`importTime` and o.`importTime` < '%s' " % (start_time, end_time)
                time_range_hos = " where '%s' < setTime and setTime < '%s' " % (start_time, end_time)

            sql_1 = "SELECT COUNT(1), SUM(cost), city, AREA FROM order_list AS o, hos_list AS d " \
                    "WHERE o.`deviceId` = d.`deviceId` %s %s GROUP BY d.`area` " % (search_w[0:-4], time_range_order)

            sql_2 = "SELECT COUNT(deviceId), COUNT(DISTINCT hosName), city, AREA FROM hos_list %s GROUP BY AREA" % \
                    time_range_hos + search_h

            sql_3 = "SELECT COUNT(importTime), city, AREA FROM maintain_repair AS o, " \
                    "hos_list AS d WHERE o.`deviceId` = d.`deviceId` %s %s  GROUP BY d.`area`" % (
                        search_w[0:-4], time_range_repair)
        else:
            param_search = {
                'd.`agentName`': user_info[2],
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_w = " and "
            for k, v in param_search.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_w += " %s = '%s'  and "
            param_search_ = {
                'd.`agentName`': user_info[2],
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_h = " and "
            for k, v in param_search_.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_h += " %s = '%s'  and "
            if None in [start_time, end_time]:
                time_range_order = None
                time_range_repair = None
                time_range_hos = 'where '
            else:
                time_range_order = " and '%s' < o.`startTime` and o.`startTime` < '%s' " % (start_time, end_time)
                time_range_repair = " and '%s' < o.`importTime` and o.`importTime` < '%s' " % (start_time, end_time)
                time_range_hos = " and '%s' < setTime and setTime < '%s' " % (start_time, end_time)

            sql_1 = "SELECT COUNT(1), SUM(cost), city, AREA FROM order_list AS o, hos_list AS d " \
                    "WHERE o.`deviceId` = d.`deviceId` AND d.`agentName` = '%s' %s %s GROUP BY d.`area` " \
                    % (user_info[2], search_w[0:-4], time_range_order)

            sql_2 = "SELECT COUNT(deviceId), COUNT(DISTINCT hosName), city, AREA FROM hos_list WHERE agentName = '%s'" \
                    " %s  GROUP BY AREA " % (user_info[2], time_range_hos + search_h)

            sql_3 = "SELECT COUNT(importTime), city, AREA FROM maintain_repair AS o, " \
                    "hos_list AS d WHERE o.`deviceId` = d.`deviceId` AND d.`agentName` = '%s' %s GROUP BY d.`area`" % \
                    (user_info[2], time_range_repair)
        data = map_data(sql_1, sql_2, sql_3)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})


class OperationalData(View):
    '''
    系统首页 运营数据概览 代理商下拉框数据
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')
        user_data = check_user_auth_level(user_phone=phone)
        if user_data[0] == '0':
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute('SELECT agentName FROM agent_list')
            data = cursor.fetchall()
            cursor.close()
            con_mysql_connect.close()
            agentList = [i[0] for i in data]
            return JsonResponse({'data': agentList, 'code': 200, 'msg': '请求成功'})
        else:
            return JsonResponse({'data': [user_data[1]], 'code': 200, 'msg': '请求成功'})


class OperationalDataSearch(View):
    '''
    运营数据概览
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql_1 = "SELECT COUNT(1), COUNT(DISTINCT hosName), city FROM hos_list GROUP BY city"
            sql_2 = "SELECT COUNT(1), city FROM order_list AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " GROUP BY d.`city`"
            sql_3 = "SELECT COUNT(1), city FROM maintain_repair AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " GROUP BY  d.`city`"
        else:
            agentName = user_info[2]
            sql_1 = "SELECT COUNT(1), COUNT(DISTINCT hosName), city FROM hos_list where agentName = '%s'GROUP BY city" \
                    % agentName
            sql_2 = "SELECT COUNT(1), city FROM order_list AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " AND o.`agentName` = '%s' GROUP BY d.`city`" % agentName

            sql_3 = "SELECT COUNT(1), city FROM maintain_repair AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " AND d.`agentName` = '%s' GROUP BY  d.`city`" % agentName
        data = table_data_by_sql(sql_1, sql_2, sql_3)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        agent_name = request.POST.get('agentName', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)

        start_time = request.POST.get('startTime', None)
        end_time = request.POST.get('endTime', None)

        if user_info[0] == '0':
            param_search = {
                'd.`agentName`': agent_name,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_w = " and "
            for k, v in param_search.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_w += " %s = '%s'  and "
            param_search_ = {
                'd.`agentName`': agent_name,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_h = " and "
            for k, v in param_search_.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_h += " %s = '%s'  and "
            if None in [start_time, end_time]:
                time_range_order = None
                time_range_repair = None
                time_range_hos = 'where '
            else:
                time_range_order = " and '%s' < o.`startTime` and o.`startTime` < '%s' " % (start_time, end_time)
                time_range_repair = " and '%s' < o.`importTime` and o.`importTime` < '%s' " % (start_time, end_time)
                time_range_hos = " where '%s' < setTime and setTime < '%s' " % (start_time, end_time)
            sql_1 = "SELECT COUNT(1), COUNT(DISTINCT hosName), city FROM hos_list %s GROUP BY city" % (
                    time_range_hos + search_h)
            sql_2 = "SELECT COUNT(1), city FROM order_list AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " %s  %s GROUP BY d.`city`" % (time_range_order, search_w)

            sql_3 = "SELECT COUNT(1), city FROM maintain_repair AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " %s %s  GROUP BY  d.`city`" % (time_range_repair, search_w)
        else:
            agent_name_user = user_info[2]

            param_search = {
                'd.`agentName`': agent_name_user,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_w = " and "
            for k, v in param_search.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_w += " %s = '%s'  and "
            param_search_ = {
                'd.`agentName`': agent_name_user,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_h = " and "
            for k, v in param_search_.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_h += " %s = '%s'  and "
            if None in [start_time, end_time]:
                time_range_order = None
                time_range_repair = None
                time_range_hos = 'where '
            else:
                time_range_order = " and '%s' < o.`startTime` and o.`startTime` < '%s' " % (start_time, end_time)
                time_range_repair = " and '%s' < o.`importTime` and o.`importTime` < '%s' " % (start_time, end_time)
                time_range_hos = " where '%s' < setTime and setTime < '%s' " % (start_time, end_time)
            sql_1 = "SELECT COUNT(1), COUNT(DISTINCT hosName), city FROM hos_list %s GROUP BY city" % (
                    time_range_hos + search_h)
            sql_2 = "SELECT COUNT(1), city FROM order_list AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " %s  %s GROUP BY d.`city`" % (time_range_order, search_w)

            sql_3 = "SELECT COUNT(1), city FROM maintain_repair AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
                    " %s %s  GROUP BY  d.`city`" % (time_range_repair, search_w)
        data = table_data_by_sql(sql_1, sql_2, sql_3)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})


class OverviewOfOperationalData(View):
    '''
    运营数据概览  订单数量 收入金额 医院数量   用户数量 维护次数
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            '''
            订单数量 收入金额 医院数量   用户数量 维护次数
            '''
            sql_1 = "SELECT COUNT(1),SUM(cost), COUNT(DISTINCT hosName), COUNT(DISTINCT userId)," \
                    " SUBSTRING(o.`startTime`, 1, 7) FROM order_list AS o, hos_list AS d" \
                    " WHERE o.`deviceId` = d.`deviceId` GROUP BY SUBSTRING(o.`startTime`, 1, 7)"

            sql_2 = "SELECT COUNT(1),SUBSTRING(importTime, 1, 7) FROM maintain_repair " \
                    "GROUP BY SUBSTRING(importTime, 1, 7)"
        else:
            agent_name = user_info[2]
            sql_1 = "SELECT COUNT(1),SUM(cost), COUNT(DISTINCT hosName), COUNT(DISTINCT userId)," \
                    " SUBSTRING(o.`startTime`, 1, 7) FROM order_list AS o, hos_list AS d" \
                    " WHERE o.`deviceId` = d.`deviceId` and o.`agentName`= '%s' " \
                    "GROUP BY SUBSTRING(o.`startTime`, 1, 7)" % agent_name

            sql_2 = "SELECT COUNT(1),SUBSTRING(importTime, 1, 7) FROM maintain_repair where agantName = '%s'" \
                    "GROUP BY SUBSTRING(importTime, 1, 7)" % agent_name
        data = func_for_get_search(sql_1, sql_2)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)

        agent_name = request.POST.get('userName', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)

        start_time = request.POST.get('startTime', None)
        end_time = request.POST.get('endTime', None)
        if user_info[0] == '0':
            param_search = {
                'd.`agentName`': agent_name,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_w = " and "
            for k, v in param_search.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_w += " %s = '%s'  and "
            if None in [start_time, end_time]:
                time_range_order = None
                time_range_repair = None
            else:
                time_range_order = " and '%s' < o.`startTime` and o.`startTime` < '%s' " % (start_time, end_time)
                time_range_repair = " and '%s' < o.`importTime` and o.`importTime` < '%s' " % (start_time, end_time)

            sql_1 = "SELECT COUNT(1),SUM(cost), COUNT(DISTINCT hosName), COUNT(DISTINCT userId)," \
                    " SUBSTRING(o.`startTime`, 1, 7) FROM order_list AS o, hos_list AS d" \
                    " WHERE o.`deviceId` = d.`deviceId` %s %s GROUP BY SUBSTRING(o.`startTime`, 1, 7)" % (
                        search_w[0:-4], time_range_order)

            sql_2 = "SELECT COUNT(1),SUBSTRING(importTime, 1, 7) FROM maintain_repair AS o, hos_list AS d " \
                    "WHERE o.`deviceId` = d.`deviceId` %s %s  GROUP BY SUBSTRING(importTime, 1, 7)" % (
                        search_w[0:-4], time_range_repair)
        else:
            agent_name = user_info[2]
            param_search = {
                'd.`agentName`': agent_name,
                'd.`province`': province,
                'd.`city`': city,
                'd.`area`': area,
            }
            search_w = " and "
            for k, v in param_search.items():
                if v is None or len(v) <= 1:
                    pass
                else:
                    search_w += " %s = '%s'  and "
            if None in [start_time, end_time]:
                time_range_order = None
                time_range_repair = None
            else:
                time_range_order = " and '%s' < o.`startTime` and o.`startTime` < '%s' " % (start_time, end_time)
                time_range_repair = " and '%s' < o.`importTime` and o.`importTime` < '%s' " % (start_time, end_time)

            sql_1 = "SELECT COUNT(1),SUM(cost), COUNT(DISTINCT hosName), COUNT(DISTINCT userId)," \
                    " SUBSTRING(o.`startTime`, 1, 7) FROM order_list AS o, hos_list AS d" \
                    " WHERE o.`deviceId` = d.`deviceId` %s %s GROUP BY SUBSTRING(o.`startTime`, 1, 7)" % (
                        search_w[0:-4], time_range_order)

            sql_2 = "SELECT COUNT(1),SUBSTRING(importTime, 1, 7) FROM maintain_repair AS o, hos_list AS d " \
                    "WHERE o.`deviceId` = d.`deviceId` %s %s  GROUP BY SUBSTRING(importTime, 1, 7)" % (
                        search_w[0:-4], time_range_repair)
        data = func_for_get_search(sql_1, sql_2)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})
