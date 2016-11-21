#!/usr/bin/env python
#
# get_users.py: retrieve and save configured users on a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Get a set of users configured in a running DC/OS cluster, and save
# them to a file in raw JSON format for backup and restore purposes.
# These can be restored into a cluster with the accompanying 
# "post_users" script.

#reference:
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/users/get_users

import sys
import os
import requests
import json
import helpers			#helper functions in separate module helpers.py

def get_users ( DCOS_IP, save_path ):
	"""
	Get the list of users from a DC/OS cluster as a JSON blob.
	Save the users to the text file in the save_path provided.
	Return the list of users as a dictionary.
	"""

	api_endpoint = '/acs/api/v1/users'
	url = 'http://'+DCOS_IP+api_endpoint
	headers = {
		'Content-type': 'application/json',
		'Authorization': 'token='+config['TOKEN'],
	}
	try:
		request = requests.get(
			url,
			headers=headers,
			)
		request.raise_for_status()
		log(
			log_level='INFO',
			operation='GET',
			object=['Users'],
			indx=0,
			content=request.status_code
			)
	except requests.exceptions.HTTPError as error:
		log(
			log_level='ERROR',
			operation='GET',
			objects=['Users'],
			indx=0,
			content=error
			)		

	#save to USERS file
	users_file = open( save_path, 'w' )
	#write to file in same raw JSON as obtained from DC/OS
	users_file.write( request.text )			
	users_file.close()	
	
	#the DC/OS API defines the users as a dict with {'array:'[]} structure
	users = json.loads( request.json )
	log(
		log_level='DEBUG',
		operation='GET',
		objects=['Users'],
		indx=0,
		content=users
		)	

	log(
		log_level='INFO',
		operation='GET',
		objects=['Users'],
		indx=0,
		content='* DONE. *'
		)	
	return dict( users )				


def get_users_groups ( DCOS_IP, save_path, users ):
	"""
	Get the list of groups that users are members of from a DC/OS cluster as a JSON blob.
	Save the users_groups to the text file in the save_path provided.
	Return the list of groups and users that belong to them as a dictionary.
	"""	

	#create a dictionary object that will hold all user-to-group memberships
	users_groups = { 'array' : [] }	

	for index, user in ( enumerate( users['array'] ) ):
		
		#append this user as a dictionary to the list 
		users_groups['array'].append(
		{
			'uid' : 		user['uid'],
			'url' : 		user['url'],
			'description' : user['description'],
			'is_remote' : 	user['is_remote'],
			'is_service' : 	user['is_service'],
			#'public_key':	user['public_key'],
			#group memberships is a list, with each member being a dictionary
			'groups' : 		[]				#initialize groups LIST for this user
		}
		)
		#get groups for this user from DC/OS
		api_endpoint = '/acs/api/v1/users/'+user['uid']+'/groups'
		url = 'http://'+DCOS_IP+api_endpoint
		try:
			request = requests.get(
				url,
				headers=headers,
				)
			request.raise_for_status()
			log(
				log_level='INFO',
				operation='GET',
				objects=['Users', 'Groups'],
				indx=index,
				content=request.status_code
				)	
		except requests.exceptions.HTTPError as error:
			log(
				log_level='ERROR',
				operation='GET',
				objects=['Users', 'Groups'],
				indx=index,
				content=error
				)	

		memberships = request.json() 	#get memberships from the JSON

		for index2, membership in ( enumerate( memberships['array'] ) ):

			#get each group membership for this user
			users_groups['array'][index]['groups'].append( 
			{
				'membershipurl' :		membership['membershipurl'],
				'group' : {
					'gid' : 			helpers.escape( membership['group']['gid'] ),
					'url' : 			membership['group']['url'],
					'description' : 	membership['group']['description']
				}
			}
			)

	#write dictionary as a JSON object to file
	users_groups_json = json.dumps( users_groups ) 		#convert to JSON
	users_groups_file = open( save_path, 'w' )
	users_groups_file.write( users_groups_json )		#write to file in raw JSON
	users_groups_file.close()									#flush

	log(
		log_level='INFO',
		operation='GET',
		objects=['Users','Groups'],
		indx=0,
		content='* DONE. *'
		)	

	return users_groups		





