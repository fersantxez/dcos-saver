#!/usr/bin/env python
#
# get_ldap.py: retrieve and save LDAP configuration from a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Get LDAP information from a DC/OS cluster and write it
# to a file in raw JSON format for backup and restore purposes.
# It can be restored into a cluster with the accompanying 
# "post_ldap" script.

#reference:
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/ldap/get_ldap_config

import sys
import os
import requests
import json
import helpers			#helper functions in separate module helpers.py

def get_ldap ( DCOS_IP, save_path ):
	"""
	Get the LDAP configuration from a DC/OS cluster as a JSON blob.
	Save it to the text file in the save_path provided.
	Return the LDAP config as a dictionary.
	"""

	#Get LDAP information from DC/OS. 
	api_endpoint = '/acs/api/v1/ldap/config'
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
			object=['LDAP'],
			indx=0,
			content=request.status_code
			)
	except requests.exceptions.HTTPError as error:
		log(
			log_level='ERROR',
			operation='GET',
			objects=['LDAP'],
			indx=0,
			content=error
			)		

	ldap_config = request.text				#raw text form requests, comes in JSON form from DC/OS

	#save to LDAP file
	ldap_file = open( config['LDAP_FILE'], 'w' )
	ldap_file.write( ldap_config )			#write to file in same raw JSON as obtained from DC/OS
	ldap_file.close()					

	log(
		log_level='INFO',
		operation='GET',
		objects=['LDAP'],
		indx=0,
		content='* DONE. *'
		)	

	return dict( ldap_config )





