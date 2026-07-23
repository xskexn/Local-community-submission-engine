from django.urls import path
from . import views

app_name = "project_management"

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_specifics, name='project_specifics'),
    path('create/', views.create_project, name='create_project'),
]