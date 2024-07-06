from django.urls import path
from my_application.views import Test_API

urlpatterns = [
    path('', Test_API.as_view()),       
    path('update', Test_API.as_view()),   
]
