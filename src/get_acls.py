#!/usr/bin/env python
# get_acls.py: retrieve and save configured ACLs on a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Get a set of ACLs configured in a running DC/OS cluster, and save
# them to a file in raw JSON format for backup and restore purposes.
# These can be restored into a cluster with the accompanying 
# "post_acls.sh" script.

#reference: 
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/permissions/get_acls

import sys
import os
import requests
import json
import helpers			#helper functions in separate module helpers.py

def get_acls ( DCOS_IP, save_path ):

	"""	Get the list of acls from a DC/OS cluster as a JSON blob.
	Save the acls to the text file in the save_path provided.
	Return the list of acls as a dictionary."""	

	api_endpoint = '/acs/api/v1/acls'
	url = 'http://'+config['DCOS_IP']+api_endpoint
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
			objects=['ACLs'],
			indx=0,
			content=request.status_code
			)
	except requests.exceptions.HTTPError as error:
		log(
			log_level='ERROR',
			operation='GET',
			objects=['ACLs'],
			indx=0,
			content=error
			)

	acls = request.text	#raw text form requests, in JSON from DC/OS

	#save to ACLs file
	acls_file = open( save_path, 'w' )
	acls_file.write( acls )			
	#write to file in same raw JSON as obtained from DC/OS
	acls_file.close()					
	log(
		log_level='INFO',
		operation='GET',
		objects=['ACLs'],
		indx=0,
		content='* DONE *'
		)

	return acls

def get_acls_permissions ( DCOS_IP, save_path, acls ):
	"""
	Get the list of Permissions for Users and Groups referenced in an ACL.
	Save the ACLs_permissions to the text file in the save_path provided.
	Return the list of permissions for users/groups as a dictionary.
	"""		


	#create a dictionary object that will hold all group-to-user memberships
	acls_permissions = { 'array' : [] }

	#loop through the list of ACLs received and get the permissions
	# /acls/{rid}/permissions
	for index, acl in ( enumerate( acls['array'] ) ):
		
		#append this acl as a dictionary to the list 
		acls_permissions['array'].append(
		{
			'rid' : 		helpers.escape( acl['rid'] ),
			'url' : 		acl['url'],
			'description' : acl['description'],
			'users' : 		[],				#initialize users LIST for this acl
			'groups':		[]				#initialize groups LIST for this acl
		}
		)

		#get permissions for this ACL from DC/OS
		#GET acls/[rid]/permissions
		api_endpoint = '/acs/api/v1/acls/'+helpers.escape( acl['rid'] )+'/permissions'
		url = 'http://'+config['DCOS_IP']+api_endpoint
		try:
			request = requests.get(
				url,
				headers=headers,
				)
			request.raise_for_status()
			log(
				log_level='INFO',
				operation='GET',
				objects=['ACLs', 'Permissions'],
				indx=index,
				content=request.status_code
				)				
		except requests.exceptions.HTTPError as error:
			log(
				log_level='ERROR',
				operation='GET',
				objects=['ACLs', 'Permissions'],
				indx=index,
				content=error
				)	

		permissions = request.json() 	#get memberships from the JSON

		#Loop through the list of user permissions and get their associated actions
		for index2, user in ( enumerate( permissions['users'] ) ):
			#get each user that is a member of this acl and append to ['users']
			acls_permissions['array'][index]['users'].append( user )
			#Loop through the list of actions for this user and get the action value
			for index3, action in ( enumerate ( user['actions'] ) ):
				#get action from DC/OS
				#GET /acls/{rid}/users/{uid}/{action}
				api_endpoint = '/acs/api/v1/acls/'+helpers.escape( acl['rid'] )+'/users/'+user['uid']+'/'+action['name']
				url = 'http://'+config['DCOS_IP']+api_endpoint
				try:
					request = requests.get(
						url,
						headers=headers,
						)
					request.raise_for_status()
					log(
						log_level='INFO',
						operation='GET',
						objects=['ACLs', 'Permissions','Users','Actions'],
						indx=index3,
						content=request.status_code
						)				
				except requests.exceptions.HTTPError as error:
					log(
						log_level='ERROR',
						operation='GET',
						objects=['ACLs', 'Permissions','Users','Actions'],
						indx=index3,
						content=error
						)	
				action_value = request.json()
				#add the value as another field of the action alongside name and url
				acls_permissions['array'][index]['users'][index2]['actions'][index3]['value'] = action_value	

		#Repeat loop with groups to get all groups and actions
		for index2, group in ( enumerate( permissions['groups'] ) ):
			#get each user that is a member of this acl and append to ['users']
			acls_permissions['array'][index]['groups'].append( group )
			#Loop through the list of actions for this user and get the action value
			for index3, action in ( enumerate ( group['actions'] ) ):
				#get action from DC/OS
				#GET /acls/{rid}/users/{uid}/{action}
				api_endpoint = '/acs/api/v1/acls/'+helpers.escape( acl['rid'] )+'/groups/'+helpers.escape( group['gid'] )+'/'+action['name']
				url = 'http://'+config['DCOS_IP']+api_endpoint
				try:
					request = requests.get(
						url,
						headers=headers,
						)
					request.raise_for_status()
					log(
						log_level='INFO',
						operation='GET',
						objects=['ACLs', 'Permissions','Groups','Actions'],
						indx=index3,
						content=request.status_code
						)		
				except requests.exceptions.HTTPError as error:
					log(
						log_level='ERROR',
						operation='GET',
						objects=['ACLs', 'Permissions','Groups','Actions'],
						indx=index3,
						content=error
						)	
				action_value = request.json()
				#add the value as another field of the action alongside name and url
				acls_permissions['array'][index]['groups'][index2]['actions'][index3]['value'] = action_value	
	#done.

	#write dictionary as a JSON object to file
	acls_permissions_json = json.dumps( acls_permissions ) 		#convert to JSON
	acls_permissions_file = open( save_path, 'w' )
	acls_permissions_file.write( acls_permissions_json )		#write to file in raw JSON
	acls_permissions_file.close()		

	log(
		log_level='INFO',
		operation='GET',
		objects=['ACLs', 'Permissions'],
		indx=0,
		content='* DONE *'
		)

	return acls_permissions
