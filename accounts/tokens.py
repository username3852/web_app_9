from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class UserRegistrationTokenGenerator(PasswordResetTokenGenerator):

  def _make_hash_value(self, user, timestamp):
   return six.text_type(user.id) + six.text_type(timestamp) + six.text_type(user.is_active)
  # takes user_id and timestamp for how long the token can be used and the active for activating the user

activation_token = UserRegistrationTokenGenerator()