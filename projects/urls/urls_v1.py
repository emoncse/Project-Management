from django.urls import path, include
from ..views import views_v1

urlpatterns = [
    path('', views_v1.dashboard, name='dashboard'),
    path('signup/', views_v1.signup, name='signup'),
    path('login/', views_v1.user_login, name='login'),
    path('create_project/', views_v1.create_project, name='create_project'),
    path('project/<int:pk>/create_task/', views_v1.create_task, name='create_task'),
    path('create_task/', views_v1.create_task, name='create_task'),
    path('user_list/', views_v1.user_list, name='user_list'),
    path('create_user/', views_v1.create_user, name='create_user'),
    path('project/<int:pk>/', views_v1.project_detail, name='project_detail'),
    path('user/<int:pk>/', views_v1.user_detail, name='user_detail'),
    path('task/<int:pk>/update_progress/', views_v1.update_task_progress, name='update_task_progress'),
    path('project/<int:pk>/add_member/', views_v1.add_member, name='add_member'),
    path('accounts/', include('django.contrib.auth.urls')),
]
