from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('project/<int:project_id>/',views.project_detail,name='project_detail'),
    path('create/', views.create_project, name='create_project'),
    path('task/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("project/<int:project_id>/usecase/", views.generate_usecase_view, name="usecase_diagram"),
    path("project/<int:project_id>/usecase/", views.usecase_diagram_view, name="usecase_diagram"),
    path("project/<int:project_id>/usecase/download/",
    views.download_usecase_diagram,
    name="download_usecase_diagram"),


]