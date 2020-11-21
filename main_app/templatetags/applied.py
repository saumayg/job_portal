from django import template
from main_app.models import Applicant

register = template.Library()

@register.simple_tag(name="applied")
def applied(job,user):
    applied = Applicant.objects.filter(job=job, user=user)
    if applied:
        return True
    else:
        return False