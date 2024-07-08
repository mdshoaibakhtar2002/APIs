from django.urls import path
from create_jobs.views import JobCreatorHandler

urlpatterns = [
    path('createjob', JobCreatorHandler.as_view()),
    path('fetchjob', JobCreatorHandler.as_view()),
]
