from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import cartpe.settings as settings
from auth_service.models import User

def send_order_confirmation_email(order_data):
    email_subject = "CartPe Order Confirmation"
    email_from = 'CartPe <%s>' % settings.EMAIL_HOST_USER
    email_to = order_data["user"]
    template = 'order_service/order_confirmation.html'

    try:
        user = User.objects.filter(email = order_data["user"]).first()

        message = {
            'subject' : email_subject,
            'order_data': order_data,
            'name': user.first_name + " " + user.last_name
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
