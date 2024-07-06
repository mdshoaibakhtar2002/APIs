from django.urls import path
from user_management.views import UserManagement, AuthenticateUser

urlpatterns = [
    path('fetchuser', UserManagement.as_view()),
    path('createuser', UserManagement.as_view()),
    path('authenticateuser', AuthenticateUser.as_view()),
]
