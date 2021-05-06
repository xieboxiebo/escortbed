from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from applet.lock_aes_func import AES_Decrypt, AES_Encrypt


class TokenView(View):
    '''
    用户反馈
    '''

    def get(self, request):
        data = request.GET.get("tokenEnstr")
        key = b"\x3A\x60\x43\x2A\x5C\x01\x21\x1F\x29\x1E\x0F\x4E\x0C\x13\x28\x25"
        aes_de_data = AES_Decrypt(key, data)
        return JsonResponse({'data': aes_de_data, 'code': 200, 'msg': 'token 解密数据，请求成功！'})

    def post(self, request):
        data = request.POST.get("tokenStr")
        key = b"\x3A\x60\x43\x2A\x5C\x01\x21\x1F\x29\x1E\x0F\x4E\x0C\x13\x28\x25"
        aes_en_data = AES_Encrypt(key, data)
        print(aes_en_data)
        return JsonResponse({'data': aes_en_data, 'code': 200, 'msg': 'token 加密数据，请求成功！'})


class LockView(View):
    '''
    用户反馈
    '''

    def get(self, request):
        data = request.GET.get("lockEnstr")
        key = b"\x3A\x60\x43\x2A\x5C\x01\x21\x1F\x29\x1E\x0F\x4E\x0C\x13\x28\x25"
        aes_de_data = AES_Decrypt(key, data)
        return JsonResponse({'data': aes_de_data, 'code': 200, 'msg': 'token 解密数据，请求成功！'})

    def post(self, request):
        data = request.POST.get("lockStr")
        key = b"\x3A\x60\x43\x2A\x5C\x01\x21\x1F\x29\x1E\x0F\x4E\x0C\x13\x28\x25"
        aes_en_data = AES_Encrypt(key, data)
        print(aes_en_data)
        return JsonResponse({'data': aes_en_data, 'code': 200, 'msg': 'token 加密数据，请求成功！'})

