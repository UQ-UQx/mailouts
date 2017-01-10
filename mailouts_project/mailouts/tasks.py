from __future__ import absolute_import

from celery import shared_task
from mailouts.models import NewsletterRecipient
from amazonses import SESMessage

@shared_task(rate_limit="4/s")
def sendsesemail(email, subject, body, body_txt, contextvars, sender, recipient_id):

	# create the message and send the email
	# the from address must be a verified sender in SES
    msg = SESMessage(sender, email, subject, body, body_txt, contextvars)
    msg.send()

	# Update database
	recipient = NewsletterRecipient.objects.get(pk=recipient_id)
    if (recipient.sent_flag==False):
        msg.send()
	    recipient.sent_flag = True
        recipient.save()
	    #print 'email sent:', email
