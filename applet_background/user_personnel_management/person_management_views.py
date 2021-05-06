from django.http import JsonResponse
from django.views import View

from applet_background.link_config import con_mysql
from user_personnel_management.func_for_person_management import check_user_auth_level, manager_list_get, \
    manager_list_data_for_search, drop_list_data, add_manager_data, phone_number_manager_name_exit


class ManagersList(View):
    '''
    平台管理员列表接口
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)  # 根据手机号获取登录者信息
        data = manager_list_get(user_info=user_info)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        pageNumber = request.POST.get('pageNumber', 1)  # 页数
        pageSize = request.POST.get('pageSize', 10)  # 每页条数
        managerName = request.POST.get('managerName', None)  # 平台管理员姓名
        managerId = request.POST.get('managerId', None)  # 平台管理员编号
        managerPhone = request.POST.get('managerPhone', None)  # 平台管理员手机
        agentName = request.POST.get('agentName', None)  # 代理商名称
        user_info = check_user_auth_level(phone)
        if user_info[0] == '0':
            pass
        else:
            agentName = user_info[1]
        dict_search = {
            'managerName': managerName, 'managerId': managerId, 'phoneNumber': managerPhone, 'agentName': agentName
        }
        data = manager_list_data_for_search(dict_search=dict_search, pageNumber=pageNumber, pageSize=pageSize)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})


class DropList(View):
    '''
    平台管理员下拉框
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)  # 根据手机号获取登录者信息
        data = drop_list_data(user_info=user_info)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        pass


class AddManager(View):
    '''
    管理员的新增和删除
    '''

    def get(self, request):
        '''
        管理员的删除
        :param request:
        :return:
        '''

        managerId = request.GET.get('managerId', None)
        managerName = request.GET.get('managerName', None)
        if None in [managerName, managerId]:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute("delete from manager_list where managerId = '%s' and managerName= '%s'",
                       (managerId, managerName))
        cursor.fetchone()
        cursor.close()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '删除成功！'})

    def post(self, request):
        '''
        管理员的新增
        :param request:
        :return:
        '''
        managerName = request.POST.get('managerName', None)
        managerPhone = request.POST.get('managerPhone', None)
        passWord = request.POST.get('passWord', None)
        agentName = request.POST.get('agentName', None)
        roleName = request.POST.get('roleName', None)
        email = request.POST.get('email')
        if None in [managerName, managerPhone, passWord, agentName, roleName, email]:
            return JsonResponse({'data': None, 'code': 300, 'msg': '参数不全！'})
        else:
            if phone_number_manager_name_exit(managerName, managerPhone) is True:
                add_manager_data(managerName, managerPhone, passWord, agentName, roleName, email)
                return JsonResponse({'data': None, 'code': 200, 'msg': '新增成功！'})
            else:
                return JsonResponse({'data': None, 'code': 300, 'msg': '用户已存在！'})


class ModifyManagerData(View):
    '''
    修改 编辑
    '''

    def get(self, request):
        phoneNum = request.GET.get('phoneNumber', None)
        managerId = request.GET.get('managerId', None)
        if None in [phoneNum, managerId]:
            return JsonResponse({'data': None, 'code': 200, 'msg': '参数不全！'})
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute(
            "select  managerName, phoneNumber, agentName, roleName from manager_list where phoneNumber = '%s'"
            " and managerId = '%s'" % (phoneNum, managerId))
        data = cursor.fetchone()
        cursor.close()
        con_mysql_connect.close()
        if len(data) < 1 or data is None:
            dict_return = {
                'managerName': None,
                'phoneNumber': None,
                'agentName': None,
                'roleName': None
            }
        else:
            dict_return = {
                'managerName': data[0],
                'phoneNumber': data[1],
                'agentName': data[2],
                'roleName': data[3]
            }
        return JsonResponse({'data': dict_return, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        managerName = request.POST.get('managerName')
        phoneNumber = request.POST.get('phoneNumber')
        roleName = request.POST.get('roleName')
        managerId = request.POST.get('managerId')  # 管理员Id
        if None in [managerId, managerName, roleName, managerId]:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})
        con_mysql_connect = con_mysql.connection()
        cursor = con_mysql_connect.cursor()
        cursor.execute("UPDATE manager_list SET managerName='%s', phoneNumber='%s', "
                       "roleName='%s' where managerId = '%s'" % (managerName, phoneNumber,
                                                                 roleName, managerId))
        cursor.fetchone()
        cursor.close()
        con_mysql_connect.close()
        return JsonResponse({'data': None, 'code': 200, 'msg': '修改成功！'})
