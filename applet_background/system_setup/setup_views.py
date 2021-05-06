import time

from django.http import JsonResponse
from django.views import View

from system_setup.func_for_setup_views import customer_service_es_data_get, customer_service_es_data_insert, \
    customer_service_es_data_delete, agree_guide_about_es_data_get, agree_guide_about_es_data_insert, \
    check_user_auth_level, feedback_data, coupon_datas_get


class CustomerService(View):
    '''
    联系客服 问题列表
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        datas, _ = customer_service_es_data_get("v2_customer_service", phone)
        if datas:
            return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})
        else:
            return JsonResponse({'data': [], 'code': 400, 'msg': '暂无数据，请插入数据后重试。'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        problem = request.POST.get("problem").strip()
        answerContent = request.POST.get("answerContent").strip()
        time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        _, problems = customer_service_es_data_get("v2_customer_service", phone)
        if problem in problems:
            return JsonResponse({'code': 400, 'msg': '添加问题已存在，请核对后重试！'})
        flag = customer_service_es_data_insert(problem, time_, answerContent, phone)
        if flag:
            return JsonResponse({'code': 200, 'msg': '添加成功！'})


class CustomerServiceDelete(View):
    '''
    联系客服 问题列表
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        datas, _ = customer_service_es_data_get("v2_customer_service", phone)
        if datas:
            return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})
        else:
            return JsonResponse({'data': [], 'code': 400, 'msg': '暂无数据，请插入数据后重试。'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        problem = request.POST.get("problem").strip()

        _, problems = customer_service_es_data_get("v2_customer_service", phone)
        if problem not in problems:
            return JsonResponse({'code': 400, 'msg': '删除问题不存在，请核对后重试！'})

        flag = customer_service_es_data_delete(problem)
        if flag:
            return JsonResponse({'code': 200, 'msg': '删除成功！'})


class UserAgreement(View):
    '''
    用户协议获取 和修改
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        datas, _ = agree_guide_about_es_data_get("v2_user_agreement", phone)
        if datas:
            return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})
        else:
            return JsonResponse({'data': [], 'code': 400, 'msg': '暂无数据，请插入数据后重试。'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        context = request.POST.get("context").strip()
        time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        _, contexts = agree_guide_about_es_data_get("v2_user_agreement", phone)
        if context in contexts:
            return JsonResponse({'code': 200, 'msg': '当前协议未发生更改，请更改后提交。'})

        flag = agree_guide_about_es_data_insert("v2_user_agreement", context, time_, phone)
        if flag:
            return JsonResponse({'code': 200, 'msg': '协议更改成功。'})



class UseGuide(View):
    '''
    使用指南
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        datas, _ = agree_guide_about_es_data_get("v2_user_guide", phone)
        if datas:
            return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})
        else:
            return JsonResponse({'data': [], 'code': 400, 'msg': '暂无数据，请插入数据后重试。'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        context = request.POST.get("context").strip()
        time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        _, contexts = agree_guide_about_es_data_get("v2_user_guide", phone)
        if context in contexts:
            return JsonResponse({'code': 200, 'msg': '当前用户指南未发生更改，请更改后提交。'})

        flag = agree_guide_about_es_data_insert("v2_user_guide", context, time_, phone)
        if flag:
            return JsonResponse({'code': 200, 'msg': '用户指南更改成功。'})


class UserFeedback(View):
    '''
    用户反馈
    '''

    def get(self, request):
        page_size = request.GET.get('pageSize', 10)
        page_number = request.GET.get('pageNumber', 1)
        phone = request.COOKIES.get('ph')  # 获取手机号
        level = check_user_auth_level(user_phone=phone)[0]

        if level[0] == "0":
            datas = feedback_data(page_size=page_size, page_number=page_number)
        else:
            agent_name = level[2]
            datas = feedback_data(agent_name=agent_name, page_size=page_size, page_number=page_number)
        return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        phoneNumber = request.POST.get('phoneNumber', None)
        isHandle = request.POST.get('isHandle', None)
        page_size = request.POST.get('pageSize', 10)
        page_number = request.POST.get('pageNumber', 1)
        phone = request.COOKIES.get('ph')  # 获取手机号
        level = check_user_auth_level(user_phone=phone)[0]
        if level[0] == "0":
            datas = feedback_data(user_phone=phoneNumber, is_handle=isHandle, page_size=page_size,
                                  page_number=page_number)
        else:
            agent_name = level[2]
            datas = feedback_data(agent_name=agent_name, user_phone=phoneNumber, is_handle=isHandle,
                                  page_size=page_size, page_number=page_number)
        return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})


class AboutUs(View):
    '''
    关于我们
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        datas, _ = agree_guide_about_es_data_get("v2_about_us", phone)
        if datas:
            return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})
        else:
            return JsonResponse({'data': [], 'code': 400, 'msg': '暂无数据，请插入数据后重试。'})

    def post(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        context = request.POST.get("context").strip()
        time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        _, contexts = agree_guide_about_es_data_get("v2_about_us", phone)
        if context in contexts:
            return JsonResponse({'code': 200, 'msg': '当前关于我们未发生更改，请更改后提交。'})

        flag = agree_guide_about_es_data_insert("v2_about_us", context, time_, phone)
        if flag:
            return JsonResponse({'code': 200, 'msg': '关于我们更改成功。'})


class CouponList(View):
    '''
    优惠券列表
    '''

    def get(self, request):
        phone = request.COOKIES.get('ph')  # 获取手机号
        level = check_user_auth_level(user_phone=phone)[0]
        if level[0] == "0":
            datas = coupon_datas_get()
        else:
            agent_id = level[1]
            datas = coupon_datas_get(agent_id=agent_id)

        return JsonResponse({'data': datas, 'code': 200, 'msg': '请求成功！'})

    def post(self, request):
        pass


class AddCoupon(View):
    '''
    新增优惠券
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class AdvertisementList(View):
    '''
    广告列表
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class AddAdvertisement(View):
    '''
    新增广告
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class MealList(View):
    '''
    套餐列表 查询
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class AddMeal(View):
    '''
    新增套餐
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass
