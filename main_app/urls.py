from django.urls import path, include
from main_app.views import *

app_name = "main_app"

urlpatterns = [
    path("",home_view,name="home"),
    path("about/",about_view,name="about"),
    path("candidate/jobs/",JobCandidateListView.as_view(),name="jobs"),
    path("jobs/<int:id>", JobDetailsView.as_view(), name="job_detail"),
    path("apply-job/<int:job_id>", ApplyJobView.as_view(), name="apply-job"),
    path("candidate/applications",EmployeeMyJobsListView.as_view(),name="applications"),
    path("company/job/create", JobCreateView.as_view(),name="new_job"),
    path("company/applicants",ApplicantsListView.as_view(),name="applicants"),
    path("company/applicant/<int:id>",ApplicantDetailsView.as_view(),name="applicant_detail",),
    path("company/applicant/<int:pk>/accept",accept,name="accept"),
    path("company/applicant/<int:pk>/reject",reject,name="reject"),
    path("company/jobs/",JobCompanyListView.as_view(),name="cjobs"),
    path("company/jobs/<int:job_id>/filled",filled,name="filled"),
]
