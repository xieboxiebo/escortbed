from django.views import View


class EquipmentAssociated(View):
    '''
    设备列表 关联列表 查询
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class EquipmentResume(View):
    '''
    设备列表 关联列表 概览
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class LockList(View):
    '''
    锁列表查询
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class LockResume(View):
    '''
    锁列表概览
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class SwitchLock(View):
    '''
    开关锁列表 查询
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class MaintainRecordList(View):
    '''
    清洗维护查询
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


class MaintainCleanFix(View):
    '''
    清洗维护确认
    '''

    def get(self, request):
        pass

    def post(self, request):
        pass


