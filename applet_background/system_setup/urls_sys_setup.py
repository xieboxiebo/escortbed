from django.urls import path

from system_setup import setup_views

urlpatterns = [
    # path()
    path('customer/', setup_views.CustomerService.as_view()),  # 系统设置——联系客服
    path('customerDel/', setup_views.CustomerServiceDelete.as_view()),  # 系统设置——联系客服——删除
    path('agreement/', setup_views.UserAgreement.as_view()),  # 用户协议
    path('guide/', setup_views.UseGuide.as_view()),  # 用户指南
    path('feedback/', setup_views.UserFeedback.as_view()),  # 用户反馈
    path('aboutUs/', setup_views.AboutUs.as_view()),  # 关于我们
    path('coupon/', setup_views.CouponList.as_view()),  # 优惠券get 删除 post
    path('coupon_add/', setup_views.AddCoupon.as_view()),  # 优惠券增加
]
