import hashlib
import time
from django.conf import settings
from amazonses import SESMessage
from mailouts.models import Subscription, StudentinCourse, Newsletter, NewsletterRecipient


def sendsesemail(email, subject, body, body_txt, contextvars, sender):

	# create the message and send the email
	# the from address must be a verified sender in SES
	msg = SESMessage(sender, email, subject, body, body_txt, contextvars)
	msg.send()

def setup_recipients(newsletter_id):
	# get newsletter object
	newsletter = Newsletter.objects.get(pk=newsletter_id)
	courses = newsletter.course_criteria
	courses_list = courses.split(',')

	# select all distinct participants that match course_criteria
	for course in courses_list:
		print 'course: ', course
		students = StudentinCourse.objects.filter(course_id=course)
		for student in students:
			#check if entry does not exist in NewsletterRecipients
			#print student.subscription.email, student.course_id, student.id
			subscription = student.subscription #Subscriptions.objects.get(pk=student.subscription_id)
			#print subscription
			if (subscription.opt_in==True):
				#print subscription.opt_in
				no_studentrecipientrecords = NewsletterRecipient.objects.filter(subscription=subscription, newsletter=newsletter).count()
				#print "no_studentrecipientrecords", no_studentrecipientrecords
				if (no_studentrecipientrecords==0):
					studentrecipientrecord = NewsletterRecipient(subscription=subscription, newsletter=newsletter, sent_flag=False)
					studentrecipientrecord.save()

def sendout_newsletter(newsletter_id):
    print 'sendout_newsletter'
    # get all recipients
    newsletter = Newsletter.objects.get(pk=newsletter_id)
    subject = newsletter.subject
    body = newsletter.email_body
    body_txt = newsletter.email_text
    sender = newsletter.sender_email

    newsletterrecipients = NewsletterRecipient.objects.filter(newsletter=newsletter, sent_flag=False)[:40000]
    print 'sendto:', len(newsletterrecipients)
    count = 0
    for recipient in newsletterrecipients:
        email = recipient.subscription.email
        name = recipient.subscription.full_name
        unsubscribe_link = make_unsubscribe_link(email)
        contextvars = {'unsubscribe_link':unsubscribe_link, 'name':name}
        sendsesemail(email, subject, body, body_txt, contextvars, sender)
        recipient.sent_flag = True
        recipient.save()
        count = count + 1
        if (count == 100):
            print count
            count = 0

def make_unsubscribe_link(email_opt_out):
	email_opt_out = email_opt_out.lower()

	validation_hash = get_md5_unsubsecret(email_opt_out)

	link = settings.UNSUBSCRIBE_SERVER_URL + '?email=' + email_opt_out + '&validation_hash=' + validation_hash
	return link

def get_md5_unsubsecret(email_opt_out):

	unsubsecret = settings.UNSUBSCRIBE_SECRET

	m = hashlib.md5()
	m.update(unsubsecret + email_opt_out)
	return m.hexdigest()
