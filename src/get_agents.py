#!/usr/bin/env python3
#
# get_agents.py: retrieve and save the agent state from a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Get the agent state from a DC/OS cluster. Save to file and provide a list of
# the Total, Active and Inactive agents.

#reference:
#http://mesos.apache.org/documentation/latest/endpoints/master/slaves/

import sys
import os
import requests
import json
import env				#environment variables and constants
import helpers			#helper functions in separate module helpers.py


def get_agents ( DCOS_IP ):
	"""
	Get the agent status configuration from a DC/OS cluster as a JSON blob.
	Save it to the text file in the save_path provided.
	Return the cluster's agent state as a dictionary.
	"""

	api_endpoint = '/mesos/slaves'
	config = helpers.get_config( env.CONFIG_FILE )	
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
		helpers.log(
			log_level='INFO',
			operation='GET',
			objects=['AGENTS'],
			indx=0,
			content=request.status_code
			)
	except requests.exceptions.HTTPError as error:
		helpers.log(
			log_level='ERROR',
			operation='GET',
			objects=['AGENTS'],
			indx=0,
			content=request.text
			)		

	#save to AGENTS file
	agents_file = open( config['AGENTS_FILE'], 'w' )
	agents_file.write( request.text )			#write to file in same raw JSON as obtained from DC/OS
	agents_file.close()				

	#Create a list of agents
	agents_dict = dict( json.loads( request.text ) )

	helpers.log(
		log_level='INFO',
		operation='GET',
		objects=['AGENTS'],
		indx=0,
		content='* DONE. *\n'
		)	

	return agents_dict


def display_agents( DCOS_IP, agents ):
	"""
	Display the status of active and inactive agents, received as a dictionary.
	"""
	agents_list = agents['slaves']

	#Display Agents - Total
	print( "Total agents: 				{0}".format( len( agents_list ) ) )
	#Display Agents - Active
	active_agents = [ agent for agent in agents_list if agent['active'] ]
	print( "Active agents: 				{0}".format( len( active_agents ) ) )
	for index, agent in ( enumerate( active_agents ) ):
		print ( "Agent #{0}: {1}".format( index, agent['hostname'] ) )
	#Display Agents - Inactive
	inactive_agents = [ agent for agent in agents_list if not agent['active'] ]
	print("Inactive agents: 			{0}".format( len( inactive_agents ) ) )
	for index, agent in ( enumerate( inactive_agents ) ):
		print ( "Agent #{0}: {1}".format( index, agent['hostname'] ) )

	input("Press ENTER to continue...")

	return True	









