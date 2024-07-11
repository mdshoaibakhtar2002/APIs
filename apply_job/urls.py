from django.urls import path
from apply_job.views import ApplyJob

urlpatterns = [
    path('applyjob', ApplyJob.as_view()),
]
