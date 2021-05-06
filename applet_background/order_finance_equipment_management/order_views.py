from django.http import JsonResponse
from django.views import View

from order_finance_equipment_management.fun_for_order import check_user_auth_level, \
    get_order_deposit_data_by_sql, get_order_data_by_sql


class DepositList(View):
    '''
    押金列表
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql = "SELECT orderId, hosName, userName,phoneNumber,amountMoney,user_payment.`agentName`," \
                  " raiseTime, status FROM user_payment , hos_list, WHERE user_payment.`deviceId` = hos_list.`deviceId`" \
                  " and user_payment.`type` = '押金' ORDER BY raiseTime DESC"
        else:
            agent_name = user_info[2]
            sql = "SELECT orderId, hosName, userName,phoneNumber,amountMoney,user_payment.`agentName`," \
                  " raiseTime, status FROM user_payment , hos_list  WHERE user_payment.`deviceId` = hos_list.`deviceId`" \
                  " and user_payment.`type` = '押金' AND user_payment.`agentName` = '%s' ORDER BY raiseTime DESC" % agent_name
        data = get_order_deposit_data_by_sql(sql)
        return JsonResponse({'data': data, 'code': 200, 'msg': '订单列表请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        user_info = check_user_auth_level(user_phone=phone)
        order_id = request.POST.get('orderId', None)
        hos_name = request.POST.get('hosName', None)
        user_name = request.POST.get('userName', None)
        status = request.POST.get('status', None)
        search_dict = {
            "user_payment.`orderId`": order_id,
            "user_payment.`userName`": user_name,
            "user_payment.`status`": status,
            "hos_list.`hoaName`": hos_name,
        }
        search_w = " and "

        if user_info[0] == '0':
            for k, v in search_dict.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    search_w += " %s = '%s' and  " % (k, v)
            sql = "SELECT orderId, hosName, userName,phoneNumber,amountMoney,user_payment.`agentName`," \
                  " raiseTime, status FROM user_payment , hos_list, WHERE user_payment.`deviceId` = hos_list.`deviceId`" \
                  " and user_payment.`type` = '押金'  %s ORDER BY raiseTime DESC" % search_w
        else:
            search_dict["user_payment.`agentName`"] = user_name[2]
            for k, v in search_dict.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    search_w += " %s = '%s' and  " % (k, v)
            sql = "SELECT orderId, hosName, userName,phoneNumber,amountMoney,user_payment.`agentName`," \
                  " raiseTime, status FROM user_payment , hos_list  WHERE user_payment.`deviceId` = hos_list.`deviceId`" \
                  " and user_payment.`type` = '押金' %s ORDER BY raiseTime DESC" % search_w
        data = get_order_deposit_data_by_sql(sql)
        return JsonResponse({'data': data, 'code': 200, 'msg': '订单列表请求成功！'})


class OrderList(View):
    '''
    订单列表
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')
        user_info = check_user_auth_level(phone)
        if user_info[0] == '0':
            sql = "SELECT orderNum, userName, phoneNumber, order_list.`deviceId`, hos_list.`hosName`, " \
                  "order_list.`agentName`, startTime, endTime,cost,couponId, orderStatus FROM order_list, " \
                  "hos_list WHERE order_list.`deviceId` = hos_list.`deviceId` ORDER BY order_list.`startTime` ASC"
        else:
            sql = "SELECT orderNum, userName, phoneNumber, order_list.`deviceId`, hos_list.`hosName`, " \
                  "order_list.`agentName`, startTime, endTime,cost,couponId, orderStatus FROM order_list, hos_list" \
                  " WHERE order_list.`deviceId` = hos_list.`deviceId` and order_list.`agentName` = '%s' " \
                  "ORDER BY order_list.`startTime` ASC" % \
                  user_info[2]

        data = get_order_data_by_sql(sql)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        phone = request.COOKIES.get('ph')
        user_info = check_user_auth_level(phone)

        user_name = request.POST.get('userName', None)
        phone_num = request.POST.get('phoneNumber', None)
        agent_name = request.POST.get('agentName', None)

        start_time = request.POST.get('startTime', None)
        end_time = request.POST.get('endTime', None)
        if user_info[0] == '0':
            search_dict = {
                "order_list.`userName`": user_name,
                "order_list.`phoneNumber`": phone_num,
                "order_list.`agentName`": agent_name,
            }
            search_w = " and "
            for k, v in search_dict.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    search_w += " %s = '%s' and  " % (k, v)
            if None in [start_time, end_time]:
                time_range = None
            else:
                time_range = " '%s' < order_list.`startTime` and  order_list.`startTime`< '%s'" % (start_time, end_time)
            sql = "SELECT orderNum, userName, phoneNumber, order_list.`deviceId`, hos_list.`hosName`, " \
                  "order_list.`agentName`, startTime, endTime,cost,couponId, orderStatus FROM order_list, " \
                  "hos_list WHERE order_list.`deviceId` = hos_list.`deviceId` %s %s ORDER BY order_list.`startTime` ASC" \
                (search_w[0:-5], time_range)
        else:
            search_dict = {
                "order_list.`userName`": user_name,
                "order_list.`phoneNumber`": phone_num,
                "order_list.`agentName`": user_info[2],
            }
            search_w = " and "
            for k, v in search_dict.items():
                if v is None or len(v) == 0:
                    pass
                else:
                    search_w += " %s = '%s' and  " % (k, v)
            if None in [start_time, end_time]:
                time_range = None
            else:
                time_range = " '%s' < order_list.`startTime` and  order_list.`startTime`< '%s'" % (start_time, end_time)
            sql = "SELECT orderNum, userName, phoneNumber, order_list.`deviceId`, hos_list.`hosName`, " \
                  "order_list.`agentName`, startTime, endTime,cost,couponId, orderStatus FROM order_list, " \
                  "hos_list WHERE order_list.`deviceId` = hos_list.`deviceId` %s %s ORDER BY order_list.`startTime` ASC" \
                (search_w[0:-5], time_range)
        data = get_order_data_by_sql(sql)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})


class RefundList(View):
    '''
    客户退款列表
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph', None)
        user_info = check_user_auth_level(user_phone=phone)
        if user_info[0] == '0':
            sql = "SELECT refund_payment.`orderNum`, refund_payment.`userName`, phoneNum, order_list.`deviceId`," \
                  " hos_list.`hosName`, refund_payment.`agentName`, order_list.`startTime`, order_list.`endTime`," \
                  "STATUS, returnReason FROM refund_payment, order_list, hos_list  WHERE refund_payment.`orderNum` " \
                  "= order_list.`orderNum` AND hos_list.`deviceId` = order_list.`deviceId` ORDER BY raiseTime"
        else:
            sql = "SELECT refund_payment.`orderNum`, refund_payment.`userName`, phoneNum, order_list.`deviceId`," \
                  " hos_list.`hosName`, refund_payment.`agentName`, order_list.`startTime`, order_list.`endTime`," \
                  "STATUS, returnReason FROM refund_payment, order_list, hos_list  WHERE refund_payment.`orderNum` " \
                  "= order_list.`orderNum` AND hos_list.`deviceId` = order_list.`deviceId` AND " \
                  "refund_payment.`agentName` = '%s' ORDER BY raiseTime" % user_info[2]

    def post(self, request):
        pass


class RefundDealReject(View):
    '''
    客户退款驳回
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class RefundDealAgree(View):
    '''
    退款审核 同意
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass
