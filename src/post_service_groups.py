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
			content=request.text
			)
		return False

	#load entire text file and convert to JSON - dictionary
	root_service_group = json.loads( service_groups_file.read() )
	service_groups_file.close()

	#'/' is a service group itself but it can't be posted directly (it exists).
	#Need to POST the groups under it (one level) that don't exist yet.
	#https://mesosphere.github.io/marathon/docs/rest-api.html#post-v2-groups


	for index, service_group in enumerate( root_service_group['groups'] ):   #don't post `/` but only his 'groups'
		helpers.format_service_group( service_group )
		service_group = helpers.single_to_double_quotes( json.dumps( service_group ) ) 
		#build the request
		api_endpoint = '/marathon/v2/groups'
		url = 'http://'+config['DCOS_IP']+api_endpoint
		headers = {
			'Content-type': 'application/json',
			'Authorization': 'token='+config['TOKEN'],
		}
		#send the request to POST the new GROUP
		try:
			request = requests.post(
				url,
				headers = headers,
				data = service_group
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
				content=request.text
			)
	
	helpers.get_input( message=env.MSG_PRESS_ENTER )

	return True