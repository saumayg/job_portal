from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from main_app.models import Job, Applicant
from main_app.forms import ApplyJobForm, CreateJobForm
from main_app.decorators import *

# Create your views here.

# Home views

def home_view(request):
    return render(request, 'main_app/home.html')

def about_view(request):
    return render(request, 'main_app/about.html')

# Job views

class JobListView(ListView):
    model = Job
    template_name = "main_app/jobs.html"
    context_object_name = "jobs"

class JobDetailsView(DetailView):
    model = Job
    template_name = "main_app/details.html"
    context_object_name = "job"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = "job_id"
    slug_url_kwarg = "job_id"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, "Successfully applied for the job!")
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy("main_app:home"))

    def get_success_url(self):
        return reverse_lazy("main_app:job_detail", kwargs={"id": self.kwargs["job_id"]})

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(
            user_id=self.request.user.id, job_id=self.kwargs["job_id"]
        )
        if applicant:
            messages.info(self.request, "You already applied for this job")
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


# Employer View

class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = "main_app/employer/applicants.html"
    context_object_name = "applicants"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs["job_id"]).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = Job.objects.get(id=self.kwargs["job_id"])
        return context


class JobCreateView(CreateView):
    template_name = "jobs/create.html"
    form_class = CreateJobForm
    extra_context = {"title": "Post New Job"}
    success_url = reverse_lazy("jobs:employer-dashboard")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy("accounts:login")
        if self.request.user.is_authenticated and self.request.user.role != "employer":
            return reverse_lazy("accounts:login")
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ApplicantsListView(ListView):
    model = Applicant
    template_name = "jobs/employer/all-applicants.html"
    context_object_name = "applicants"

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id)


@login_required(login_url=reverse_lazy("accounts:login"))
def filled(request, job_id=None):
    try:
        job = Job.objects.get(user_id=request.user.id, id=job_id)
        job.filled = True
        job.save()
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy("jobs:employer-dashboard"))
    return HttpResponseRedirect(reverse_lazy("jobs:employer-dashboard"))


# Employee View

@method_decorator(
    login_required(login_url=reverse_lazy("accounts:login")), name="dispatch"
)
@method_decorator(user_is_employee, name="dispatch")
class EmployeeMyJobsListView(ListView):
    model = Applicant
    template_name = "main_app/employee/applications.html"
    context_object_name = "applicants"

    def get_queryset(self):
        self.queryset = (
            self.model.objects.select_related("job")
            .filter(user_id=self.request.user.id)
            .order_by("-created_at")
        )
        if (
            "status" in self.request.GET
            and len(self.request.GET.get("status")) > 0
            and int(self.request.GET.get("status")) > 0
        ):
            self.queryset = self.queryset.filter(
                status=int(self.request.GET.get("status"))
            )
        return self.queryset