from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# from jobsapp.views import EditProfileView
from accounts.views import *

app_name = "accounts"

urlpatterns = [
    path("candidate/register", RegisterEmployeeView.as_view(), name="employee_register"),
    path("company/register", RegisterEmployerView.as_view(), name="employer_register"),
    # path(
    #     "employee/profile/update",
    #     EditProfileView.as_view(),
    #     name="employer-profile-update",
    # ),
    path("logout", LogoutView.as_view(), name="logout"),
    path("login", LoginView.as_view(), name="login"),
]