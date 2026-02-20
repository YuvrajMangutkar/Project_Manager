from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('project/<int:project_id>/',views.project_detail,name='project_detail'),
    path('create/', views.create_project, name='create_project'),
    path('task/complete/<int:task_id>/', views.complete_task, name='complete_task'),


]