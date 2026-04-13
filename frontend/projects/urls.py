from django.urls import path, re_path
from . import views

urlpatterns=[
    # --- Django Classic Auth & Exports & Diagrams ---
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('project/<int:project_id>/gantt/', views.gantt_view, name='gantt_view'),
    path('project/<int:project_id>/export/pdf/', views.export_pdf_view, name='export_pdf'),
    path("project/<int:project_id>/usecase/", views.usecase_diagram_view, name="usecase_diagram"),
    path("project/<int:project_id>/dfd-level0/", views.dfd_level0_view, name="dfd_level0"),
    path("project/<int:project_id>/dfd-level1/", views.dfd_level1_view, name="dfd_level1"),
    path("project/<int:project_id>/activity/", views.activity_diagram_view, name="activity_diagram"),
    path("debug/groq/", views.groq_debug_view, name="groq_debug"),
    path("download-diagram/", views.download_diagram, name="download_diagram"),

    # --- JSON APIs for React ---
    path('api/projects/', views.api_dashboard, name='api_dashboard'),
    path('api/projects/<int:project_id>/', views.api_project_detail, name='api_project_detail'),
    path('api/projects/create/', views.api_create_project, name='api_create_project'),
    path('api/tasks/<int:task_id>/complete/', views.api_complete_task, name='api_complete_task'),
    path('api/projects/<int:project_id>/chat/', views.ai_chat_api, name='ai_chat_api'),
    path('api/tasks/<int:task_id>/scaffold/', views.task_scaffold_api, name='task_scaffold'),
    
    # Old views preserved under different names (optional) or mapped to API above.
    
    # --- React SPA Fallback ---
    # Map React UI paths to the React rendering view
    path('', views.react_app, name='dashboard'),
    path('dashboard', views.react_app),
    path('create', views.react_app, name='create_project'),
    path('project/<int:project_id>', views.react_app, name='project_detail'),
]