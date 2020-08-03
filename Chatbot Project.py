Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 22:45:29) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import json
import requests
from datetime import datetime
from dateutil import parser # pip install python-dateutil
from pytz import timezone   # pip install pytz
# https://www.youtube.com/watch?v=BI4HxHn1HmQ
# i have used pytz for time zone 
# to install pytz, use this comand : easy_install --upgrade pytz
# this was the site where i have found about pytz : http://pytz.sourceforge.net/

# dateutil is also required. it is used for parsing dates.


# a function that changes timezoe of a date and returns a datetime object converted into the specified timezone
def change_timezone_of_datetime_object(date_time_object, new_timezone_name):
    """Return the *date_time_object* with it's timezone changed to *new_timezone_name*

    :param date_time_object: The datetime object whose timezone is to be changed
    :param new_timezone_name: The name of the timezone to which the *date_time_object* is to be changed to
    """
    #https://www.youtube.com/watch?v=zY02utxcauo for Parsing and Formatting Dates in Python With Datetime
	#  for the new_timezone
    new_timezone_object = timezone(new_timezone_name)
    # it will update our  timezone of the datetime in object 
    date_time_object = date_time_object.astimezone(new_timezone_object)
    # Return the converted datetime object
    return date_time_object



# this is the  URL of our API means base url
api_end_point = 'https://api.list.co.uk/v1/events'

# a variable to store our API key
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZWY1ODFkMjYtY2Q3NC00Yzg1LTgzMTQtNDY0MzRlZTlmODAwIiwia2V5X2lkIjoiZWYzZjczZGUtODkwMy00MjkxLTlkZjEtYzA2MDIyNWVlZTcwIiwiaWF0IjoxNTg0Njk1NTQ2fQ.9jD_DmWBhdMcPVFglPXtR1XIpgGDi9pLSfYt5_MFVO8"

# (from the docmentation guide)a variable to create headers for the request
headers = {
	"Authorization": "Bearer " + api_key
}
#i have watched youtube video to understand https://www.youtube.com/watch?v=g4wdm488mkE
# to call API and store the respose returned in a variable
response = requests.get(api_end_point, headers = headers)

# convert our string and display the returned response text as JSON
event_list = json.loads(response.text)

event_count = 1

label_prefix = "|_ "

# i have used for and if command to use print my events
for event in event_list:
	print("\n\nEVENT # %d " % event_count, end='')
	print("-"*80) # just a line to separate the events

	print(label_prefix + "Name : " + event['name'])
	print(label_prefix + "Sort Name : " + event['sort_name'])
	print(label_prefix + "Status : " + event['status'])

	for descr in event['descriptions']:
		if descr['type'] == "third-party":
			print(label_prefix + "Description : " + descr['description'])

	place = event['schedules'][0]['place']['name']
	place_address = event['schedules'][0]['place']['address'] + ", " + event['schedules'][0]['place']['town']
	place_address += " - " + event['schedules'][0]['place']['postal_code']

	print(label_prefix + "Place : " + place)
	print(label_prefix + "\t Address : " + place_address)

	# parse the string date using dateutil parser
	dt = parser.parse(event['schedules'][0]['start_ts']) 
	# covert the UTC datetime to local datetime
	dt = change_timezone_of_datetime_object(dt, 'Europe/London')
	print(label_prefix + "Start time : " + dt.ctime())  # use the converted datetime object

	dt = parser.parse(event['schedules'][0]['end_ts'])
	dt = change_timezone_of_datetime_object(dt, 'Europe/London')
	print(label_prefix + "End time : " + dt.ctime())


	# for ticket summury if event has ticket info 
	if "ticket_summary" in event['schedules'][0]:
		print(label_prefix + "Ticket Range : " + event['schedules'][0]['ticket_summary'])
	else:
		print(label_prefix + "Ticket Range : NOT SPECIFIED!")


	performance_count = len(event['schedules'][0]['performances'])
	print("\n %d performances found..." % performance_count)

	performance_count = 1
	#  to print performance info
	for performance in event['schedules'][0]['performances']:
		print(label_prefix + "\t Performance #%d" % performance_count)

		dt = parser.parse(performance['ts'])
		dt = change_timezone_of_datetime_object(dt, 'Europe/London')
		print(label_prefix + "\t\t Start time : " + dt.ctime())

		performance_count += 1

	event_count += 1 
exitline=input("ënter to exit")
print ("Thats all we Got")
