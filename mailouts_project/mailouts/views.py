from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from datetime import datetime
from django.utils.dateparse import parse_datetime
import csv
import os

from .models import Subscriptions, StudentinCourse

def index(request):
	template = loader.get_template('index.html')
	contextvars = {}

	#context = RequestContext(request, contextvars)
	response = HttpResponse(template.render(contextvars, request))
	response['P3P'] = 'CP="We do not have a P3P policy."'
	return response

def import_csv(request):

	template = loader.get_template('import_csv.html')
	contextvars = {}

	dirname = os.path.dirname(os.path.abspath(__file__))
	filename = os.path.join(dirname, 'data', 'uqx-email_opt_in-prod-analytics.csv')

	# Update the DB based on the csv file
	csv2db(filename)

	#context = RequestContext(request, contextvars)
	response = HttpResponse(template.render(contextvars, request))
	response['P3P'] = 'CP="We do not have a P3P policy."'
	return response
	
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

	
