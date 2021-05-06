import datetime

from django.http import JsonResponse
from django.views import View

from applet_background.link_config import con_mysql
from participate_hospital_management.func_for_hospital import check_user_auth_level, search_hospital_data, \
    search_hospital_department_data


class HospitalListData(View):
    '''
    医院列表数据
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        data = search_hospital_data(user_info=user_info)
        return JsonResponse({'data': data, 'code': 200, 'msg': '医院列表数据请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        hosName = request.POST.get('hosName', None)  # 医院名称
        agentName = request.POST.get('agentName', None)  # 代理商名称
        agentPhone = request.POST.get('agentPhone', None)  # 代理商手机号
        modeName = request.POST.get('modeName', None)  # 套餐名称
        search_dict = {
            'hosName': hosName,
            'agentName': agentName,
            'agentPhone': agentPhone,
            'modeName': modeName
        }
        user_info = check_user_auth_level(user_phone=phone)
        data = search_hospital_data(user_info=user_info, search_dict=search_dict)
        return JsonResponse({'data': data, 'code': 200, 'msg': '医院列表数据请求成功！'})


class AddHospitalData(View):
    '''
    新增医院
    '''

    def get(self, request):
        '''
        get请求 返回套餐名称
        :param request:
        :return:
        '''
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute("SELECT modeName, modeId FROM mode_list")
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        mode_list = list()
        for mode in data:
            mode_list.append({
                'modeName': mode[0],
                'modeId': mode[1]
            })
        return JsonResponse({'data': mode_list, 'code': 200, 'msg': '套餐下拉列表！'})

    def post(self, request):
        '''
        该接口完善
        :param request:
        :return:
        '''
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)

        hosName = request.POST.get('hosName', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)
        addr = request.POST.get('addr', None)
        modeId = request.POST.get('modeId', None)
        modeName = request.POST.get('modeName', None)
        ratio = request.POST.get('ratio', None)
        if None in [hosName, province, city, area, addr, modeId, modeName, ratio]:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        else:
            hosId = '{0:%f%d%m%y%M%S}'.format(datetime.datetime.now())
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute("insert into hos_name (hosName,hosId, agentId, agentName, province, city, area,"
                           " addr, modeName, modeId, hosRatio) values ('%s','%s','%s','%s','%s','%s','%s',"
                           "'%s','%s','%s','%s',)" % (
                               hosName, hosId, user_info[1], user_info[2], province, city, area, addr,
                               modeName, modeId, ratio))
            cursor.fetchone()
            cursor.close()
            con_mysql_connect.commit()
            con_mysql_connect.close()
            return JsonResponse({'data': None, 'code': 200, 'msg': '新增成功！'})


class UpdateHospitalData(View):
    '''
    修改医院信息/和新增一样
    '''

    def get(self, request):
        return JsonResponse({'data': None, 'code': 200, 'msg': '暂无该接口！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)

        hosName = request.POST.get('hosName', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)
        addr = request.POST.get('addr', None)
        modeId = request.POST.get('modeId', None)
        modeName = request.POST.get('modeName', None)
        ratio = request.POST.get('ratio', None)
        if None in []:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        else:
            hosId = '{0:%f%d%m%y%M%S}'.format(datetime.datetime.now())
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute("insert into hos_name (hosName,hosId, agentId, agentName, province, city, area,"
                           " addr, modeName, modeId, ratio) values ('%s','%s','%s','%s','%s','%s','%s',"
                           "'%s','%s','%s','%s',)" % (
                               hosName, hosId, user_info[1], user_info[2], province, city, area, addr,
                               modeName, modeId, ratio))
            cursor.fetchone()
            cursor.close()
            con_mysql_connect.commit()
            con_mysql_connect.close()
            return JsonResponse({'data': None, 'code': 200, 'msg': '新增成功！'})


class DeleteHospitalData(View):
    '''
    根据医院名删除医院
    '''

    def get(self, request):
        pass

    def post(self, request):
        '''
        根据医院名删除医院
        :param request:
        :return:
        '''
        hos_name = request.POST.get('hosName', None)
        if hos_name is None:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute("delete from hos_name where hos_name = '%s'", hos_name)
        cursor.fetchone()
        cursor.close()
        con_mysql_connect.commit()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '删除成功！'})


# ---------------科室数据------

class DepartmentListData(View):
    '''
    科室列表数据
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql = "SELECT hosName, agentName, hosDepartM ," \
                  "addr, COUNT(deviceId) FROM hos_list GROUP BY hosDepartM, hosName"
        else:
            sql = "SELECT hosName, agentName, hosDepartM ,addr," \
                  " agentName,COUNT(deviceId) FROM hos_list where agentId = '%s' GROUP BY hosDepartM, hosName" \
                  % user_info[1]
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.commit()
        con_mysql_connect.close()
        data_depart = list()
        for hos_depart in data:
            data_depart.append({
                'hosName': hos_depart[0],
                'agentName': hos_depart[1],
                'hosDepartM': hos_depart[2],
                'addr': hos_depart[3],
                'count': hos_depart[4]
            })
        return JsonResponse({'data': data_depart, 'code': 200, 'msg': '科室列表！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)

        hosName = request.POST.get('hosName', None)
        agentName = request.POST.get('agentName', None)
        hosDeportM = request.POST.get('hosDeportM', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        area = request.POST.get('area', None)
        addr = request.POST.get('addr', None)

        search_parm = {
            'hosName': hosName,
            'agentName': agentName,
            'hosDepartM': hosDeportM,
            'province': province,
            'city': city,
            'area': area,
            'addr': addr
        }
        data = search_hospital_department_data(user_info=user_info, search_dict=search_parm)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功'})


class AddDepartmentData(View):
    '''
    新增科室
    '''

    def get(self, request):
        '''
        新增 代理商下拉列表
        :param request:
        :return:
        '''
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql = "select hosName, hosId, agentName, agentId from hos_name "
        else:
            sql = "select hosName, hosId, agentName, agentId from hos_name where agentId = '%s'" % user_info[1]
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        return_data = list()
        for data_ in data:
            return_data.append({
                'hosName': data_[0],
                'hosId': data_[1],
                'agentName': data_[2],
                'agentId': data_[3]
            })
        return JsonResponse({'data': return_data, 'code': 200, 'msg': '下拉列表请求成功！'})

    def post(self, request):
        '''
        新增科室数据
        :param request:
        :return:
        '''
        hos_name = request.POST.get('hosName', None)
        hos_id = request.POST.get('hosId', None)
        agent_name = request.POST.get('agentName', None)
        agent_id = request.POST.get('agentId', None)
        department_name = request.POST.get('departmentName', None)

        sql = "select province, city, area, addr from department_list"
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        sql_2 = "insert into department_list (hosName,hosId, agentName, agentId,departmentName, province, city," \
                " AREA, addr) values ('%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s')" \
                % (hos_name, hos_id, agent_name, agent_id, department_name, data[0], data[1], data[2], data[3])
        cursor.execute(sql_2)
        cursor.close()
        con_mysql_connect.commit()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '请求成功！'})


class UpdateDepartmentData(View):
    '''
    修改科室信息
    '''

    def get(self, request):
        pass

    def post(self, request):
        '''
        科室信息修改
        :param request:
        :return:
        '''
        hos_name = request.POST.get('hosName', None)
        hos_id = request.POST.get('hosId', None)
        agent_name = request.POST.get('agentName', None)
        agent_id = request.POST.get('agentId', None)
        department_name = request.POST.get('departmentName', None)
        if None in [hos_name, hos_id, agent_name, agent_id, department_name]:
            return JsonResponse({'data': None, 'code': 500, 'msg': '新增是失败！'})

        sql = "select province, city, area, addr from department_list"
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        sql_2 = "insert into department_list (hosName,hosId, agentName, agentId,departmentName, province, city," \
                " AREA, addr) values ('%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s')" \
                % (hos_name, hos_id, agent_name, agent_id, department_name, data[0], data[1], data[2], data[3])
        cursor.execute(sql_2)
        cursor.close()
        con_mysql_connect.commit()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '新增成功！'})


class DeleteDepartmentData(View):
    '''
    删除科室
    '''

    def get(self, request):
        pass

    def post(self, request):
        hos_name = request.POST.get('hosName', None)
        agent_name = request.POST.get('agentName', None)
        department_name = request.POST.get('departmentName', None)
        if None in [hos_name, agent_name, department_name]:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        sql = "delete from department_list where " \
              "hosName = '%s' and departmentName = '%s' and agentName = '%s'" \
              % (hos_name, department_name, agent_name)
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        cursor.fetchone()
        cursor.close()
        con_mysql_connect.commit()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '删除成功！'})


# -------------床位数据---

class BunkListData(View):
    '''
    床位列表数据
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql = "select bedId, agentId, agentName, firm, bindStatus  from bed_list "
        else:
            sql = "select bedId, agentId, agentName, firm, bindStatus from bed_list where agentId = '%s'" % user_info[1]
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        return_data = list()
        for data_ in data:
            return_data.append({
                'bedId': data_[0],
                'agentId': data_[1],
                'agentName': data_[2],
                'firm': data_[3],
                'bindStatus': data_[4]
            })
        return JsonResponse({'data': return_data, 'code': 200, 'msg': '床设备'})

    def post(self, request):
        '''
        床位列表 查询
        :param request:
        :return:
        '''
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        bed_id = request.POST.get('bedId', None)
        bind_status = request.POST.get('bindStatus', None)
        agent_name = request.POST.get('agentName', None)
        search_word = {
            'bindStatus': bind_status,
            'bedId': bed_id,
            'agentName': agent_name,
        }
        str_search = 'and '
        for k, v in search_word.items():
            if v is None or len(v) == 0:
                pass
            else:
                str_ = "  %s = '%s'  and " % (k, v)
                str_search += str_
        str_search = str_search[0:-4]
        if user_info[0] == '0':
            if len(str_search) < 3:
                sql = "select bedId, agentId, agentName, firm, bindStatus  from bed_list "
            else:
                sql = "select bedId, agentId, agentName, firm, bindStatus  from bed_list where %s" % str_search[3:]
        else:
            sql = "select bedId, agentId, agentName, firm, bindStatus from bed_list where agentId = %s %s" \
                  % (user_info[1], str_search)
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        con_mysql_connect.close()
        return_data = list()
        for data_ in data:
            return_data.append({
                'bedId': data_[0],
                'agentId': data_[1],
                'agentName': data_[2],
                'firm': data_[3],
                'bindStatus': data_[4]
            })
        return JsonResponse({'data': return_data, 'code': 200, 'msg': '床设备'})


class AddBunkData(View):
    '''
    新增床位
    '''

    def get(self, request):
        pass

    def post(self, request):
        bed_id = request.POST.get('bedId', None)
        agent_name = request.POST.get('agentName', None)
        agent_id = request.POST.get('agentId', None)
        firm = request.POST.get('firm', None)
        if None in [bed_id, agent_name, agent_id, firm]:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute("insert into bed_list (bedId, agentId, agentName, firm) VALUES ('%s','%s','%s','%s','%s')",
                       bed_id, agent_id, agent_name, firm)
        cursor.fetchone()
        cursor.close()
        con_mysql_connect.commit()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '新增成功！'})


class UpdateBunkData(View):
    '''
    修改床位信息
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class DeleteBunkData(View):
    '''
    删除床位
    '''

    def get(self, request):
        pass

    def post(self, request):
        bed_id = request.POST.get('bedId', None)
        agent_name = request.POST.get('agentName', None)
        if None in [bed_id, agent_name]:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute("delete from bed_list where bedId = '%s' and agentName = '%s'", bed_id, agent_name)
        cursor.fetchone()
        cursor.close()
        con_mysql_connect.commit()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '删除成功！'})


class ExcelDataInsertIntoSys(View):
    '''
    通过excel数据导入
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass
