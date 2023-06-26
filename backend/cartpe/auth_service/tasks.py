from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from auth_service.email import send_verification_email

logger = get_task_logger(__name__)

@shared_task
def send_verification_email_task(user_email):
    logger.info("Received email - '%s' from RegisterUserAPIView" % user_email)
    logger.info("Sending verification email to %s" % user_email)

    response = send_verification_email(user_email=user_email)

    if response['status'] == 400:
        logger.error("Email was not sent because of errors")
        return "Verification email was not sent"

    return "Successfully sent verification email to %s" % user_email