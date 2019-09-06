from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('testbed_status', views.testbed_status, name='testbed_status'),
    path('user_jobs', views.user_jobs, name='user_jobs'),
    path('view_all_jobs', views.view_all_jobs, name='view_all_jobs'),
    path('all_jobs', views.get_all_jobs, name='all_jobs'),
    path('get_logs', views.get_logs, name='get_logs'),
    path('get_job_details', views.get_job_details, name='get_job_details'),
    path('display_testbed_info', views.display_testbed_info,name='display_testbed_info'),
    path('view_msgs', views.view_msgs, name='view_msgs'),
    path('get_msgs', views.get_msgs, name='get_msgs'),
    path('add_new_testbed', views.add_new_testbed, name='add_new_testbed'),

]
