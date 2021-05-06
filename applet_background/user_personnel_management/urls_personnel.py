from django.urls import path

from user_personnel_management import person_management_views

urlpatterns = [
    path('mangersList/', person_management_views.ManagersList.as_view()),  # 管理员下拉列表
    path('dropList/', person_management_views.DropList.as_view()),  # 下拉列表
    path('managerAddDel/', person_management_views.AddManager.as_view()),  # 新增/删除管理员接口
    path('managerModify/', person_management_views.ModifyManagerData.as_view()),  # 管理员修改
]
