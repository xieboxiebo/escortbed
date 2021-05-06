from django.http import JsonResponse
from django.views import View

from user_personnel_management.func_for_users_managent import check_user_auth_level, search_user_list_data


class UserDataSearch(View):
    '''
    客户数据/ 搜索
    '''

    def get(self, request):
        data = search_user_list_data()
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        page_number = request.POST.get('pageNumber', 1)
        page_size = request.POST.get('pageSize', 10)
        userName = request.POST.get('userName', None)
        phoneNumber = request.POST.get('phoneNumber', None)
        deposit = request.POST.get('deposit', None)
        search_dict = {
            'userName': userName,
            'phoneNumber': phoneNumber,
            'deposit': deposit
        }
        data = search_user_list_data(page_number=page_number, page_size=page_size, search_dict=search_dict)
        return JsonResponse({'data': data, 'code': 200, 'msg': '请求成功！'})
