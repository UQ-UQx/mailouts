from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import csv
import os
import hashlib

from .models import Subscriptions, StudentinCourse

def index(request):
	return render(request, 'index.html', {})

def unsubscribe(request):
	contextvars = {}

	# TODO: change email_opt_out to the user who received the email
	email_opt_out = 'uqx.courses@gmail.com'
	base_url = request.get_host()
	contextvars['link'] = base_url + '/' + make_unsubscribe_link(email_opt_out)

	return render(request, 'unsubscribe.html', contextvars)

def make_unsubscribe_link(email_opt_out):
	email_opt_out = email_opt_out.lower()

	validation_hash = get_md5_unsubsecret()

	link = 'mailouts/unsubscribe/' + email_opt_out + '/' + validation_hash + '/'
	return link

def updateoptout_db(request, email, validation_hash):
	contextvars = {}
	contextvars['title'] = 'Unsubscribe result'

	expected = get_md5_unsubsecret()

	if expected != validation_hash:
		contextvars['content'] = 'Invalid un-subscribe link used.'
	else:
		opt_in = False
		opt_in_source = 'unsubscribe_link'
		preference_set_datetime = timezone.now()
		Subscriptions.objects.filter(email=email).update(opt_in=opt_in, opt_in_source=opt_in_source, preference_set_datetime=preference_set_datetime)
		contextvars['content'] = 'Unsubscription from UQx Mailing List Successful.'

	return render(request, 'base_page.html', contextvars)


def get_md5_unsubsecret():
	if "UNSUBSCRIBE_SECRET" in os.environ:
		unsubsecret = os.environ['UNSUBSCRIBE_SECRET']
	else:
		unsubsecret = 'secret unsubscribe'

	m = hashlib.md5()
	m.update(unsubsecret)
	return m.hexdigest()

def import_csv(request):
	contextvars = {}

	dirname = os.path.dirname(os.path.abspath(__file__))
	filename = os.path.join(dirname, 'data', 'uqx-email_opt_in-prod-analytics.csv')

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
				subscription, subscription_created = Subscriptions.objects.get_or_create(
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

	
