from django.urls import path

from participate_hospital_management import agent_participate_views

urlpatterns = [
    path('agent/', agent_participate_views.AgentListData.as_view()),  # 代理商列表
    path('addDel/', agent_participate_views.AddDelAgent.as_view()),  # 新增代理商
    path('update/', agent_participate_views.UpdateAgentData.as_view()),  # 代理商信息修改

]
