from django.urls import path, include
from main_app.views import *

app_name = "main_app"

urlpatterns = [
    path("",home_view,name="home"),
    path("about/",about_view,name="about"),
    path("jobs/",JobListView.as_view(),name="jobs"),
    path("jobs/<int:id>", JobDetailsView.as_view(), name="jobs-detail"),
    path("apply-job/<int:job_id>", ApplyJobView.as_view(), name="apply-job"),
]
