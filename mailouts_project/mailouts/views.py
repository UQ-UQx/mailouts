from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import csv
import os
import hashlib
from django.conf import settings
from amazonses import SESMessage
from emailutils import *

from .models import Subscription, StudentinCourse, Newsletter, NewsletterRecipient

def setuprecipients(request):

	newsletter_id = request.GET.get('newsletter_id')

	setup_recipients(newsletter_id)

	message =  "The recipients have been setup for Newsletter " + newsletter_id

	contextvars = {'message': message, 'page_title': "Setup Newsletter Recipients"}

	return render(request, 'setuprecipients.html', contextvars)

#todo: make an admin task and trigger as an async celery task
def sendnewsletters(request):
	newsletter_id = request.GET.get('newsletter_id')

	sendout_newsletter(newsletter_id)

	message = "The email newsletter have been sent out. (id=" + newsletter_id + ")"

	contextvars = {'message': message, 'page_title': "Send Email Newsletter"}

	return render(request, 'sendnewsletters.html', contextvars)

def newsletter(request):
	#get distinct list of courses
	course_list = list(set(StudentinCourse.objects.values_list('course_id', flat=True)))

	page_title = "Newsletter"
	email_body = ""
	subject = ""
	numberofrecipients = 0

	#print make_unsubscribe_link('aneesha.bakharia@gmail.com')
	setup_recipients(1)
	sendout_newsletter(1)

	contextvars = {'course_list': course_list, 'page_title': page_title, 'email_body': email_body, 'subject': subject, 'numberofrecipients': numberofrecipients}

	return render(request, 'newsletter.html', contextvars)

def newsletterpreview(request):

	email_body = ''
	contextvars = {'email_body': email_body}

	name = 'Aneesha'
	subject = 'Hello from SES Test'
	body = 'Hello {{name}} <br/> {{unsubscribe_link}}'
	recipient = 'a.bakharia1@uq.edu.au'

	unsubscribe_link = make_unsubscribe_link(recipient)


	# create the message and send the email
	# the from address must be a verified sender in SES
	msg = SESMessage('a.bakharia1@uq.edu.au', recipient, subject, body, body, {'name':name, 'unsubscribe_link':unsubscribe_link})
	#msg.text = body
	#msg.html = body + ' html'
	msg.send()

	return render(request, 'newletterpreview.html', contextvars)

def unsubscribe(request):
	contextvars = {}

	# TODO: change email_opt_out to the user who received the email
	email_opt_out = 'uqx.courses@gmail.com'
	base_url = request.get_host()
	contextvars['link'] = base_url + '/' + make_unsubscribe_link(email_opt_out)

	return render(request, 'unsubscribe.html', contextvars)

def updateoptout_db(request, email, validation_hash):
	contextvars = {}
	contextvars['title'] = 'Unsubscribe result'

	expected = get_md5_unsubsecret(email)

	if expected != validation_hash:
		contextvars['content'] = 'Invalid un-subscribe link used.'
	else:
		opt_in = False
		opt_in_source = 'unsubscribe_link'
		preference_set_datetime = timezone.now()
		Subscriptions.objects.filter(email=email).update(opt_in=opt_in, opt_in_source=opt_in_source, preference_set_datetime=preference_set_datetime)
		contextvars['content'] = 'Unsubscription from UQx Mailing List Successful.'

	return render(request, 'base_page.html', contextvars)

def import_csv(request):
	contextvars = {}

	dirname = os.path.dirname(os.path.abspath(__file__))
	filename = settings.OPT_IN_CSVFILE

	# Update the DB based on the csv file
	csv2db(filename)

	return render(request, 'import_csv.html', contextvars)

def csv2db(filename):
	with open(filename, 'rU') as csvfile:
		filereader = csv.reader(csvfile)
		# Skip header
		headers = filereader.next()

		for row in filereader:
			email = row[0]
			full_name = row[1]
			course_id = row[2]
			opt_in = row[3]
			opt_in_source = 'edxlog'
			preference_set_datetime = format_datetime(row[4])

			if preference_set_datetime:
				subscription, subscription_created = Subscription.objects.get_or_create(
					email = email,
					defaults = {'opt_in': opt_in, 'opt_in_source': opt_in_source, 'preference_set_datetime': preference_set_datetime, 'full_name': full_name}
				)

				if not subscription_created:
					# Update this record if the current data is more recent
					if subscription.preference_set_datetime < preference_set_datetime:
						subscription.opt_in = opt_in
						subscription.opt_in_source = opt_in_source
						subscription.preference_set_datetime = preference_set_datetime
						subscription.full_name = full_name
						subscription.save()

				studentincourse, studentincourse_created = StudentinCourse.objects.get_or_create(
					subscription = subscription,
					course_id = course_id
				)
			else:
				print 'email: ' + email + ' preference_set_datetime: ' + row[4] + ' BAD. Not processed to this record.'

def format_datetime(date_time):
	#print date_time
	if len(date_time) == 19:
		date_time = date_time + '+0000'
	elif len(date_time) == 25:
		#remove ':' in date_time
		date_time = date_time[:22] + date_time[23:]
	else:
		return False

	datetime_object = parse_datetime(date_time)
	return datetime_object
