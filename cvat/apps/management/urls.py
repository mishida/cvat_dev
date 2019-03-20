from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create/', views.UserCreateView.as_view(), name='users_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='users_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='users_delete'),
    path('users/<int:pk>/projects/', views.assigned_projects, name='assigned_projects'),
    path('users/<int:pk>/projects/deassign/', views.dessign_user_project, name='dessign_user_project'),

    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='projects_create'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='projects_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='projects_delete'),
    path('projects/<int:pk>/datasets/', views.DatasetsView.as_view(), name='datasets'),
    path('projects/<int:pk>/datasets/create/', views.DatasetCreateView.as_view(), name='datasets_create'),
    path('projects/<int:project_id>/datasets/<int:pk>/update/', views.DatasetUpdateView.as_view(), name='datasets_update'),
    path('projects/<int:project_id>/datasets/<int:pk>/delete/', views.DatasetDelateView.as_view(), name='datasets_delete'),
    path('projects/<int:project_id>/datasets/<int:dataset_id>/tasks/', views.TasksView.as_view(), name='tasks'),
    path('projects/<int:pk>/labels/', views.labels, name='labels'),
]
