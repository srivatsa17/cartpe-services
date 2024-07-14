from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from auth_service.email import send_verification_email, send_reset_password_email

logger = get_task_logger(__name__)


@shared_task
def send_verification_email_task(user_email):
    logger.info(f"Received email - '{user_email}' from RegisterUserAPIView")
    logger.info(f"Sending verification email to {user_email}")

    response = send_verification_email(user_email=user_email)

    if response["status"] == 400:
        logger.error("Email was not sent because of errors")
        logger.error(response)
        return "Verification email was not sent"

    return f"Successfully sent verification email to {user_email}"


@shared_task
def send_reset_password_email_task(user_email):
    logger.info(f"Received email - '{user_email}' from ResetPasswordRequestAPIView")
    logger.info(f"Sending reset password email to {user_email}")

    response = send_reset_password_email(user_email=user_email)

    if response["status"] == 400:
        logger.error("Email was not sent because of errors.")
        logger.error(response)
        return "Reset password email was not sent."

    return f"Successfully sent reset password email to {user_email}"
