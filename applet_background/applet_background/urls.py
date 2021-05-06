"""applet_background URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('home/', include('system_home.urls_system')),  # 系统首页
    path('user/', include('user_personnel_management.urls_user')),  # 用户管理
    path('person/', include('user_personnel_management.urls_personnel')),  # 人员管理

    path('participate/', include('participate_hospital_management.urls_participate')),  # 加盟管理
    path('hospital/', include('participate_hospital_management.urls_hospital')),  # 医院管理

    path('order/', include('order_finance_equipment_management.urls_order')),  # 订单管理
    path('finance/', include('order_finance_equipment_management.urls_finance')),  # 财务中心
    path('equipment/', include('order_finance_equipment_management.urls_equipment')),  # 设备管理

    path('system/', include('system_setup.urls_sys_setup')),  # 系统设置

    path('applet/', include('applet.urls_app')),  # 系统设置

]

'''
create_time: 2020.08.18
author  : ljx
Q&A email: U2FsdGVkX1+aRrNwHGgWMeZcRzI2yyLprowhXcZiN7IgvZRcVRmMpQA/TssA5352  AES: ljx@

'''
