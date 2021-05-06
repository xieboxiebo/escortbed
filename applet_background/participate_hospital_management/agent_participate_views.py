# 加盟管理
import uuid

from django.http import JsonResponse
from django.views import View

from applet_background.link_config import con_mysql
from participate_hospital_management.func_for_agent import search_for_agent_data_list, check_user_auth_level


class AgentListData(View):
    '''
    代理商列表查询
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)  # 根据手机号获取登录者信息
        if user_info[0] == '0':
            data = search_for_agent_data_list()
            return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})
        else:
            return JsonResponse({'data': None, 'code': 500, 'msg': '权限不够！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)  # 根据手机号获取登录者信息
        agentId = request.POST.get('agentId', None)
        agentName = request.POST.get('agentName', None)
        agentPhone = request.POST.get('agentPhone', None)
        dict_search = {
            'agentId': agentId,
            'agentName': agentName,
            'agentPhone': agentPhone
        }
        if user_info[0] == '0':
            data = search_for_agent_data_list(dict_search=dict_search)
            return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})
        else:
            return JsonResponse({'data': None, 'code': 500, 'msg': '权限不够！'})


class AddDelAgent(View):
    '''
    新增/删除 代理商
    '''

    def get(self, request):
        '''
        删除代理商
        :param request:
        :return:
        '''
        agentId = request.GET.get('agentId', None)
        agentName = request.GET.get('agentName', None)
        if None not in [agentId, agentName]:
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute("delete from agent_list where agentName = '%s' and agentId = '%s'", agentName, agentId)
            cursor.fetchone()
            cursor.close()
            con_mysql_connect.close()
            return JsonResponse({'data': None, 'code': 200, 'msg': '已删除'})
        else:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全'})

    def post(self, request):
        '''
        新增代理商
        :param request:
        :return:
        '''
        agentName = request.POST.get('agentName', None)
        agentPhone = request.POST.get('agentPhone', None)
        account = request.POST.get('account', None)
        ratio = request.POST.get('ratio', None)
        agentId = uuid.uuid1()
        if None not in [agentName, agentId, agentPhone, account, ratio]:
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute("insert into agent_list (agentName, agentPhone, account,ratio,agentId) values"
                           " ('%s','%s','%s','%s','%s',)", agentName, agentPhone, account, ratio, agentId)
            cursor.fetchone()
            cursor.close()
            con_mysql_connect.close()
            return JsonResponse({'data': None, 'code': 200, 'msg': '新增成功！'})
        else:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})


class UpdateAgentData(View):
    '''
    编辑修改代理商
    '''

    def get(self, request):
        pass

    def post(self, request):
        '''
        修改代理商信息
        :param request:
        :return:
        '''
        agentId = request.POST.get('agentId', None)
        agentName = request.POST.get('agentName', None)
        agentPhone = request.POST.get('agentPhone', None)
        account = request.POST.get('account', None)
        ratio = request.POST.get('ratio', None)

        if None not in [agentName, agentPhone, account, ratio, agentId]:
            con_mysql_connect = con_mysql.connection()
            cursor = con_mysql_connect.cursor()
            cursor.execute("update agent_list agentName = '%s', agentPhone='%s', account='%s', ratio='%s' "
                           "where agentId = '%s'", agentName, agentPhone, account, ratio, agentId)
            cursor.fetchone()
            for table in ['ad_list', 'bed_list', 'hos_list', 'lock_list', 'manager_list', 'mode_list', 'refund_payment',
                          'user_payment']:
                cursor.execute("update %s agentName=%s where agentId='%s'", table, agentName, agentId)
                cursor.fetchall()
            cursor.close()
            con_mysql_connect.close()
            return JsonResponse({'data': None, 'code': 200, 'msg': '修改成功！'})
        else:
            return JsonResponse({'data': None, 'code': 500, 'msg': '参数不全！'})


class TransactionList(View):
    '''
    交易列表 区分管理员和代理商
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)  # 根据手机号获取登录者信息

    def post(self, request):
        pass


# ----------------------提现订单列表----------

class TransactionStatistics(View):
    '''
    交易统计
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass
