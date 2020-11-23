from django import forms

from main_app.models import Job, Applicant

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ("job",)

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = (
            "user",
            "created_at",
        )
        labels = {
            "last_date": "Last Date",
            "company_name": "Company Name",
            "company_description": "Company Description",
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job

class AddCommentForm(forms.ModelForm):
    labels = {
        "comment": "Add a comment"
    }

    class Meta:
        model = Applicant
        fields = ("comment"),
