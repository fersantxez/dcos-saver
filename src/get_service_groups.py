#!/usr/bin/env python3
#
# get_service_groups.py: retrieve and save configured service groups on a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Get a set of Marathon service groups groups configured in a running DC/OS cluster, and save
# them to a file in raw JSON format for backup and restore purposes.
# These can be restored into a cluster with the accompanying 
# "post_service_groups.py" script.

#reference:
#https://mesosphere.github.io/marathon/docs/rest-api.html

import sys
import os
import requests
import json
import env				#environment variables and constants
import helpers			#helper functions in separate module helpers.py

def get_service_groups ( DCOS_IP ):

	"""	
	Get the list of service groups from a DC/OS cluster as a JSON blob.
	Save the service groups to the text file in the save_path provided.
	Return the list of service groups as a dictionary.
	"""

	api_endpoint = '/marathon/v2/groups'
	config = helpers.get_config( env.CONFIG_FILE )
	url = 'http://'+config['DCOS_IP']+api_endpoint	
	headers = {
		'Content-type': 'application/json',
		'Authorization': 'token='+config['TOKEN']
	}
	try:
		request = requests.get(
			url,
			headers=headers,
			)
		request.raise_for_status()
		helpers.log(
			log_level='INFO',
			operation='GET',
			objects=['Service Groups'],
			indx=0,
			content=request.status_code
			)
	except requests.exceptions.HTTPError as error:
		helpers.log(
			log_level='ERROR',
			operation='GET',
			objects=['Service Groups'],
			indx=0,
			content=request.text
			)

	service_groups = request.text
	service_groups_file = open( env.SERVICE_GROUPS_FILE, 'w' )
	service_groups_file.write( service_groups )			
	service_groups_file.close()					
	helpers.log(
		log_level='INFO',
		operation='GET',
		objects=['Service Groups'],
		indx=0,
		content='* DONE *'
		)	
	service_groups_dict = dict( json.loads( service_groups ) )
	
	return service_groups_dict
