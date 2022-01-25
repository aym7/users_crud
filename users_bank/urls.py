"""users_handler URL Configuration
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.api_root),

    path("users/", views.CustomerList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.CustomerDetail.as_view(), name="user-detail"),

    path("admins/", views.UserList.as_view(), name='admin-list'),
    path("admins/<int:pk>/", views.UserDetail.as_view(), name="admin-detail"),
]

