from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from order_service.email import send_order_confirmation_email

logger = get_task_logger(__name__)

@shared_task
def send_order_confirmation_email_task(order_data):
    logger.debug("Received data - '%s' from OrderAPIView" % order_data)
    logger.info("Sending verification email to %s" % order_data["user"])

    response = send_order_confirmation_email(order_data=order_data)

    if response['status'] == 400:
        logger.error("Email was not sent because of errors")
        logger.error(response)
        return "Order confirmation email was not sent"

    return "Successfully sent order confirmation email to %s" % order_data["user"]
