#!/usr/bin/env python
#
# post_groups.py: load from file and restore groups to a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Post a set of groups to a running DC/OS cluster, read from a file 
# where they're stored in raw JSON format as received from the accompanying
#"get_groups.py" script.

#reference:
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/groups/put_groups_gid

import sys
import os
import requests
import json
import helpers      #helper functions in separate module helpers.py

def post_groups ( DCOS_IP, load_path ):
	""" 
	Get the Group information from the load_path provided as an argument,
	and post it to a DC/OS cluster available at the DCOS_IP argument.
	"""

	try:  	
		#open the GROUPS file and load the LIST of groups from JSON
		groups_file = open( load_path, 'r' )
		log(
			log_level='INFO',
			operation='LOAD',
			objects=['Groups'],
			indx=0,
			content='** OK **'
			)
	except IOError as error:
		log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Groups'],
			indx=0,
			content=error
			)
		return False

	#load entire text file and convert to JSON - dictionary
	groups = json.loads( groups_file.read() )
	groups_file.close()

	#loop through the list of groups and
	#PUT /groups/{gid}
	for index, group in ( enumerate( groups['array'] ) ): 

		gid = helpers.escape( group['gid'] )
		#build the request
		api_endpoint = '/acs/api/v1/groups/'+gid
		url = 'http://'+config['DCOS_IP']+api_endpoint
		headers = {
		'Content-type': 'application/json',
		'Authorization': 'token='+config['TOKEN'],
		}
		data = {
		'description': group['description'],
		}
		#send the request to PUT the new USER
		try:
			request = requests.put(
			url,
			data = json.dumps( data ),
			headers = headers
			)
			request.raise_for_status()
			#show progress after request
			log(
				log_level='INFO',
				operation='PUT',
				objects=['Groups: '+gid],
				indx=0,
				content=request.status_code
				)
		except requests.exceptions.HTTPError as error:
			log(
				log_level='ERROR',
				operation='PUT',
				objects=['Groups: '+gid],
				indx=0,
				content=request.status_code
				)

	return True
	

def post_groups_users( DCOS_IP, load_path ):
	""" 
	Get the list of groups_users from the load_path provided as an argument,
	and post it to a DC/OS cluster available at the DCOS_IP argument.
	"""

	try:  	
		#open the GROUPS file and load the LIST of groups from JSON
		groups_file = open( load_path, 'r' )
		log(
			log_level='INFO',
			operation='LOAD',
			objects=['Groups', 'Users'],
			indx=0,
			content='** OK **'
			)
	except IOError as error:
		log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Groups', 'Users'],
			indx=0,
			content=error
			)
		return False

	#load entire text file and convert to JSON - dictionary
	groups_users = json.loads( groups_users_file.read() )
	groups_users_file.close()

	for index, group_user in ( enumerate( groups_users['array'] ) ): 
		#PUT /groups/{gid}/users/{uid}
		gid = helpers.escape( group_user['gid'] )	

		#array of users for this group_users
		for index2, user in ( enumerate( group_user['users'] ) ): 

			uid = user['user']['uid']
			#build the request
			api_endpoint = '/acs/api/v1/groups/'+gid+'/users/'+uid
			url = 'http://'+config['DCOS_IP']+api_endpoint
			headers = {
			'Content-type': 'application/json',
			'Authorization': 'token='+config['TOKEN'],
			}
			#send the request to PUT the new USER
			try:
				request = requests.put(
				url,
				headers = headers
				)
				request.raise_for_status()
				#show progress after request
				log(
					log_level='INFO',
					operation='PUT',
					objects=[ 'Groups: '+gid,'Users: '+uid ],
					indx=index2,
					content=request.status_code
					)	
			except requests.exceptions.HTTPError as error:
				log(
					log_level='ERROR',
					operation='PUT',
					objects=[ 'Groups: '+gid,'Users: '+uid ],
					indx=index2,
					content=error
					)	

	log(
		log_level='INFO',
		operation='PUT',
		objects=['Groups','Users'],
		indx=0,
		content='* DONE *'
		)
	
	return True	

