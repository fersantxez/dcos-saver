#!/usr/bin/env python3
#
# post_service_groups.py: load from file and restore Marathon service groups to a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Post a set of service groups to a running DC/OS cluster, read from a file 
# where they're stored in raw JSON format as received from the accompanying
# "get_service_groups.py" script.

#reference:
#https://mesosphere.github.io/marathon/docs/rest-api.html

import sys
import os
import requests
import json
import env        #environment variables and constants
import helpers      #helper functions in separate module helpers.py

def post_service_groups ( DCOS_IP ):
	""" 
	Get the Service Group information from the service groups file,
	and post it to a DC/OS cluster available at the DCOS_IP argument.
	"""

	config = helpers.get_config( env.CONFIG_FILE )
	try:  	
		#open the SERVICE GROUPS file and load the LIST of groups from JSON
		service_groups_file = open( env.SERVICE_GROUPS_FILE, 'r' )
		helpers.log(
			log_level='INFO',
			operation='LOAD',
			objects=['Service Groups'],
			indx=0,
			content='** OK **'
			)
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Service Groups'],
			indx=0,
			content=error
			)
		return False

	#load entire text file and convert to JSON - dictionary
	service_groups = json.loads( service_groups_file.read() )
	service_groups_file.close()

	#remove apps from the service group tree as we can't put both apps and groups in a request
	helpers.remove_apps_from_service_group( service_group )
	#build the request
	api_endpoint = '/marathon/v2/groups'
	url = 'http://'+config['DCOS_IP']+api_endpoint
	headers = {
		'Content-type': 'application/json',
		'Authorization': 'token='+config['TOKEN'],
	}
	data = service_group
	#send the request to PUT the new GROUP
	try:
		request = requests.post(
			url,
			headers = headers,
			data = json.dumps( data )
		)
		request.raise_for_status()
		#show progress after request
		helpers.log(
			log_level='INFO',
			operation='PUT',
			objects=['Service Groups'],
			indx=0,
			content=request.status_code
		)
	except requests.exceptions.HTTPError as error:
		helpers.log(
			log_level='ERROR',
			operation='PUT',
			objects=['Service Groups'],
			indx=0,
			content=request.status_code
		)
		return False

	return True