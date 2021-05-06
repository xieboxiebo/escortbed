from django.urls import path

from user_personnel_management import person_management_views
from user_personnel_management import users_management_views

urlpatterns = [
    path('managers/', person_management_views.ManagersList.as_view()),  # 平台管理员列表接口
    path('drop/', person_management_views.DropList.as_view()),  # 平台管理员下拉框
    path('addDel/', person_management_views.AddManager.as_view()),  # 管理员的新增和删除
    path('modify/', person_management_views.ModifyManagerData.as_view()),  # 修改

    path('users/', users_management_views.UserDataSearch.as_view())  # 用户管理 用户列表

]
