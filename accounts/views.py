from django.shortcuts import render, HttpResponse
from django.views import View #vanilla view basically for the CRUD operation
from accounts.forms import UserRegistrationForm

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from accounts.tokens import activation_token

from django.contrib.auth.models import User

# Create your views here.


class UserRegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm() #for vanilla view we create object for a class
        template_name = "accounts/signup.html"
        return render(request, template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid(): # the django itself will lookupon the constraints for validation
            user = form.save(commit=False) # not to save in db directly
            user.is_active = False # initially it is set to false
            user.save()
            message_subject = "Activate your account"
            domain_url = get_current_site(request) # request garney ko domain_url
            user_email = form.cleaned_data["email"] # only extracting the clean email
            message = render_to_string(  # whle we send the message it is similar like returning render with other parameters
                "accounts/activation_message.html",
                {
                    "domain": domain_url.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.id)), #first change to bytes so that comp can read and then encode
                    "token": activation_token.make_token(user),
                },
            )

            email = EmailMessage(message_subject, message, to=[user_email]) # here u can add other reqd. fields such as cc, bcc etc.
            email.send()
            activation_msg = "Open your email to activate the account."
            return render(
                request, "accounts/activate_email.html", {"activation_msg": activation_msg} # no need for urls since it is a part of activate fn
            )

        template_name = "accounts/signup.html"
        return render(request, template_name, {"form": form})


def activate(request, uidb64, token): # to activate the flag ie. user active
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid) #query based on id of userid ie select * from objects where id = uid
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "accounts/activation_success.html")
    return render(request, "accounts/activation_fail.html")