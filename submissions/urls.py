from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    path("", views.submission_list, name="submission_list"),
    path("create/", views.create_submission, name="create_submission"),
    path('delete/<int:pk>/', views.delete_submission, name='delete_submission'),
]
