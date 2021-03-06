from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.managers import UserManager

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))

# Create your models here.
class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12,error_messages={"required":"Role must be provided"})
    gender = models.CharField(max_length=10, blank=True,null=True,default="")
    email = models.EmailField(unique=True,blank=False,error_messages={"unique":"A user with that email already exists"})
    mobile = models.CharField(max_length=50,blank=True, null=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    cpi = models.CharField(max_length=50, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]

    def __unicode__(self):
        return self.email

    objects = UserManager()