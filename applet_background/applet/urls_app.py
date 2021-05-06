from django.urls import path

from applet import views

urlpatterns = [
    # path()
    path('token/', views.TokenView.as_view()),  # 获取token数据
    path('lock/', views.LockView.as_view()),  # 锁加密解密

]
