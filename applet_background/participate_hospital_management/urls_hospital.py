from django.urls import path

from participate_hospital_management import hospital_join_views

urlpatterns = [
    path('hosList/', hospital_join_views.HospitalListData.as_view()),  # 医院列表数据
    path('hosAdd/', hospital_join_views.AddHospitalData.as_view()),  # 新增医院
    path('hoaUpdate/', hospital_join_views.UpdateHospitalData.as_view()),  # 修改医院信息
    path('hosDel/', hospital_join_views.DeleteHospitalData.as_view()),  # 删除医院

    path('depList/', hospital_join_views.DepartmentListData.as_view()),  # 科室列表数据
    path('depAdd/', hospital_join_views.AddDepartmentData.as_view()),  # 新增科室
    path('depUpdate/', hospital_join_views.UpdateDepartmentData.as_view()),  # 修改科室信息
    path('depDel/', hospital_join_views.DeleteDepartmentData.as_view()),  # 删除科室

    path('bedList/', hospital_join_views.BunkListData.as_view()),  # 床位列表信息
    path('bedAdd/', hospital_join_views.AddBunkData.as_view()),  # 新增床位
    path('bedDel/', hospital_join_views.DeleteBunkData.as_view()),  # 删除床位

]
