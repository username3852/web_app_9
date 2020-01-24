from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import User


class UserRegistrationForm(UserCreationForm):
  # It is not mandatory to create separate form.py and can be included in views.py but to make code clean we did this 
  
  class Meta:
    model   = User
    fields  = ("first_name", "last_name", "email", "username") #password is given default by django

    def clean_email(self): # ie. each user is validated by the the email existing in the db . if already exist then not allowing it
      data = self.cleaned_data["email"]
      try:
        user_email = User.objects.get(email=data)
      except User.DoesNotExist:
        pass
      else:
        raise forms.ValidationError("Email already exist")

      def clean_contact_no(self):
        data = self.cleaned_data["contact_no"]
        for i in data:
          if not (i.isdigit()or i in "+-"):
            raise forms.ValidationError("Invalid contact number")