from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import cartpe.settings as settings
from auth_service.models import User
from auth_service.token import account_activation_token

def send_verification_email(user_email):
    email_subject = "Verify your Email"
    email_from = 'CartPe <%s>' % settings.EMAIL_HOST_USER
    email_to = user_email
    template = 'auth_service/email_verification.html'

    try:
        if not User.objects.filter(email = user_email).exists():
            return { "status" : 400 }

        user = User.objects.get(email = user_email)
        current_site = "localhost:3000"             # TODO: To be changed once frontend url is configured

        message = {
            'subject' : email_subject,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user)
        }
        html_content = render_to_string(template_name = template, context = message)
        text_content = strip_tags(html_content)

        email_message = EmailMultiAlternatives(
            subject = email_subject,
            body = text_content,
            from_email = email_from,
            to = [email_to]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        response = { "status" : 200 }

    except Exception as e:
        response = { "status" : 400, "error": str(e) }

    return response