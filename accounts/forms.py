from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
  
  class Meta:
    model   = User
    fields  = ("first_name", "last_name", "email", "username") #password is given default by django

# It is not mandatory to create separate form.py and can be included in views.py but to make code clean we did this 