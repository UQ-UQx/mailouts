import hashlib
import time
from django.conf import settings
from amazonses import SESMessage
from mailouts.models import Subscriptions, StudentinCourse, Newsletters, NewsletterRecipients


def sendsesemail(email, subject, body, contextvars, sender):
	'''
	name = 'Aneesha'
	subject = 'Hello from SES Test'
	body = 'Hello {{name}} <br/> {{unsubscribe_link}}'
	recipient = 'test@test.edu.au'

	unsubscribe_link = make_unsubscribe_link(recipient)
	'''

	# create the message and send the email
	# the from address must be a verified sender in SES
	msg = SESMessage(sender, email, subject, body, body, contextvars)
	#msg.text = body
	#msg.html = body + ' html'
	#print msg.preview('html')
	msg.send()
	print 'email sent:', email


def setup_recipients(newsletter_id):
	# get newsletter object
	newsletter = Newsletters.objects.get(pk=newsletter_id)
	courses = newsletter.course_criteria
	courses_list = courses.split(',')

	# select all distinct participants that match course_criteria
	for course in courses_list:
		students = StudentinCourse.objects.filter(course_id=course)
		for student in students:
			#check if entry does not exist in NewsletterRecipients
			#print student
			subscription = Subscriptions.objects.get(pk=student.subscription_id)
			#print subscription
			if (subscription.opt_in==True):
				no_studentrecipientrecords = NewsletterRecipients.objects.filter(subscription_id=subscription, newsletter_id=newsletter).count()
				if (no_studentrecipientrecords==0):
					studentrecipientrecord = NewsletterRecipients(subscription_id=subscription, newsletter_id=newsletter, sent_flag=False)
					studentrecipientrecord.save()

def sendout_newsletter(newsletter_id):
	# get all recipients
	newsletter = Newsletters.objects.get(pk=newsletter_id)
	subject = newsletter.subject
	body = newsletter.email_body
	sender = newsletter.sender_email

	newsletterrecipients = NewsletterRecipients.objects.filter(newsletter_id=newsletter, sent_flag=False)
	count = 0
	for recipient in newsletterrecipients:
		email = recipient.subscription_id.email
		print email
		#name = recipient.subscription_id.name
		unsubscribe_link = make_unsubscribe_link(email)
		contextvars = {'unsubscribe_link':unsubscribe_link}
		sendsesemail(email, subject, body, contextvars, sender)
		recipient.sent_flag = 1
		recipient.save()
		count = count + 1
		if (count == 10):
			count = 0
			time.sleep(1)

def make_unsubscribe_link(email_opt_out):
	email_opt_out = email_opt_out.lower()

	validation_hash = get_md5_unsubsecret(email_opt_out)

	link = 'https://tools.ceit.uq.edu.au/uqxmailouts/unsubscribe/index.php?email=' + email_opt_out + '&validation_hash=' + validation_hash
	return link

def get_md5_unsubsecret(email_opt_out):
	print settings.UNSUBSCRIBE_SECRET
	unsubsecret = settings.UNSUBSCRIBE_SECRET

	m = hashlib.md5()
	m.update(unsubsecret + email_opt_out)
	return m.hexdigest()
