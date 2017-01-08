#!/usr/bin/env python
#
# post_acls.py: load from file and restore ACLs to a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Post a set of ACLs to a running DC/OS cluster, read from a file 
# where they're stored in raw JSON format as received from the accompanying
# "get_acls.sh" script.

#reference:
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/permissions/put_acls_rid
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/permissions/put_acls_rid_users_uid_action


import sys
import os
import requests
import json
import env        #environment variables and constants
import helpers      #helper functions in separate module helpers.py

def post_acls ( DCOS_IP ):
	"""
	Get the ACL information from the ACLs file path specified in the env parameters,
	and post it to a DC/OS cluster available at the DCOS_IP argument.
	"""	

	config = helpers.get_config( env.CONFIG_FILE )	
	try:  	
		#open the ACLS file and load the LIST of acls from JSON
		acls_file = open( env.ACLS_FILE, 'r' )
		helpers.log(
			log_level='INFO',
			operation='LOAD',
			objects=['ACLs'],
			indx=0,
			content='** OK **'
			)
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['ACLs'],
			indx=0,
			content=error
			)
		return False

	#load entire text file and convert to JSON - dictionary
	acls = json.loads( acls_file.read() )
	acls_file.close()

	#loop through the list of ACL Rules and
	#PUT /acls/{rid}
	for index, acl in ( enumerate( acls['array'] ) ): 

		rid = helpers.escape( acl['rid'] )
		#build the request
		api_endpoint = '/acs/api/v1/acls/'+rid
		url = 'http://'+config['DCOS_IP']+api_endpoint
		headers = {
		'Content-type': 'application/json',
		'Authorization': 'token='+config['TOKEN'],
		}
		data = {
		'description': acl['description'],
		}
		#send the request to PUT the new USER
		try:
			request = requests.put(
			url,
		 	headers = headers,
		 	data = json.dumps( data )
			)
			request.raise_for_status()
			#show progress after request
			helpers.log(
				log_level='INFO',
				operation='PUT',
				objects=['ACLs: '+rid],
				indx=0,
				content=request.status_code
				)
		except requests.exceptions.HTTPError as error:
			helpers.log(
				log_level='ERROR',
				operation='PUT',
				objects=['ACLs: '+rid],
				indx=0,
				content=request.status_code
				)
	
	return True

def post_acls_permissions( DCOS_IP ):
	"""
	Get the list of acls_permissions from the load_path in the environment parameters,
	and post it to a DC/OS cluster available at the DCOS_IP argument.
	"""
	#loop through the list of ACL permission rules and create the ACLS in the system
	#/acls/{rid}/groups/{gid}/{action}
	#/acls/{rid}/users/{uid}/{action}

	config = helpers.get_config( env.CONFIG_FILE )
	try:  	
		#open the GROUPS file and load the LIST of groups from JSON
		acls_permissions_file = open( env.ACLS_FILE, 'r' )
		helpers.log(
			log_level='INFO',
			operation='LOAD',
			objects=['ACLs', 'Permissions'],
			indx=0,
			content='** OK **'
			)
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['ACLs', 'Permissions'],
			indx=0,
			content=error
			)
		return False

	#load entire text file and convert to JSON - dictionary
	acls_permissions = json.loads( acls_permissions_file.read() )
	acls_permissions_file.close()

	for index, acl_permission in ( enumerate( acls_permissions['array'] ) ): 
		rid = helpers.escape( acl_permission['rid'] )	

		#array of users for this acl_permission
		for index2, user in ( enumerate( acl_permission['users'] ) ): 
		#PUT  /acls/{rid}/users/{uid}/{action}

			uid = user['uid']
			#array of actions for this user_acl_permission
			for index3, action in ( enumerate( user['actions'] ) ): 

				name = helpers.escape( action['name'] )
				#build the request
				api_endpoint = '/acs/api/v1/acls/'+rid+'/users/'+uid+'/'+name
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
					helpers.log(
						log_level='INFO',
						operation='PUT',
						objects=[ 'ACLs: '+rid,'Users: '+uid ],
						indx=index2,
						content=request.status_code
						)	
				except requests.exceptions.HTTPError as error:
					helpers.log(
						log_level='ERROR',
						operation='PUT',
						objects=[ 'ACLs: '+rid,'Users: '+uid ],
						indx=index2,
						content=error
						)

		#array of groups for this acl_permission
		for index2, group in ( enumerate( acl_permission['groups'] ) ): 
		#PUT  /acls/{rid}/groups/{gid}/{action}

			gid = helpers.escape( group['gid'] )
			#array of actions for this group_acl_permission
			for index3, action in ( enumerate( group['actions'] ) ): 

				name = helpers.escape( action['name'] )
				#build the request
				api_endpoint = '/acs/api/v1/acls/'+rid+'/groups/'+gid+'/'+name
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
					helpers.log(
						log_level='INFO',
						operation='PUT',
						objects=[ 'ACLs: '+rid,'Groups: '+gid ],
						indx=index2,
						content=request.status_code
						)	
				except requests.exceptions.HTTPError as error:
					helpers.log(
						log_level='ERROR',
						operation='PUT',
						objects=[ 'ACLs: '+rid,'Groups: '+gid ],
						indx=index2,
						content=error
						)	
		
	helpers.log(
		log_level='INFO',
		operation='PUT',
		objects=['ACLs','Permissions'],
		indx=0,
		content='* DONE *'
		)

	return True

