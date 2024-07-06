from django.urls import path
from user_management.views import UserManagement

urlpatterns = [
    path('', UserManagement.as_view()),
]
