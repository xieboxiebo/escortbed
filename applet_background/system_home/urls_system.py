from django.urls import path

from system_home import system_views

# 上级路由 home
urlpatterns = [
    path(r'login/', system_views.BackgroundLogin.as_view()),  # 管理员登陆接口

    path(r'drop/', system_views.DropDownList.as_view()),  # 首页 代理商信息下拉选项参数
    path(r'static/', system_views.GeneralStatistics.as_view()),  # 首页 代理商信息 统计表上
    path(r'equipment/', system_views.EquipmentState.as_view()),  # 首页 代理商信息 设备统计图
    path(r'consumption/', system_views.ConsumptionState.as_view()),  # 首页 代理商信息 消费统计图
    path(r'Operational/', system_views.OperationalData.as_view()),  # 首页 运营数据概览 下拉列表数据

    # 消费订单/设备状态统计图 echars
]
