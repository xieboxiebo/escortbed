from django.views import View


class DataSalesAndUses(View):
    '''
    大数据分析页面 销售 用户分析
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class DataMealAndIncome(View):
    '''
    大数据分析页面 月销售额和套餐比列
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class DataOrderList(View):
    '''
    大数据分析 实时订单信息
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class DataQuotaAndArea(View):
    '''
    大数据分析 销售额和地区
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class DataAgentAnalysis(View):
    '''
    大数据分析 代理商销售分析
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class OrderList(View):
    '''
    消费订单列表 数据查找
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class WithdrawalOperation(View):
    '''
    消费订单列表 提现操作
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class WithdrawalList(View):
    '''
    提现订单列表 查询
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class ExamineWithdrawal(View):
    '''
    提现订单列表审核  提现审核审批 支付
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class RefundList(View):
    '''
    退款明细
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass
