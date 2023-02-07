from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.is_active) + str(user.pk) + str(timestamp)
        )

email_verification_token = EmailVerificationTokenGenerator()


def send_email_verification(request:HttpRequest, user: get_user_model(), email_from = 'hillarykisera@gmail.com'):
    domain = get_current_site(request).domain
    subject = 'Activate Your Account'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    body = render_to_string(
            'accounts/email_verification.html',
            {
                'name': f"{user.first_name} {user.last_name}",
                'domain': domain,
                'uid': uid,
                'token': token,
            }
        )

    if EmailMessage(to=[user.email], subject=subject, body=body).send() == 1:
        return True
    else:
        return False

def get_user_from_email_verification_token(uidb64, token: str):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist) as err:
        user = None

    if user != None and email_verification_token.check_token(user, token):
        return user

    return None