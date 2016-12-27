#!/usr/bin/env python3

# run.py: interactively receive and store the configuration for backup/restore
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# This set of scripts allows to backup and restore several configurations from
# a running DC/OS Cluster. It uses the DC/OS REST API as Documented here:
# https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/
#
# A $PWD/DATA directory is created to store all information backed up from the cluster
# All files in this DATA directory are encoded in raw JSON. The restore scripts read
# these files, extract the relevant fields and post them back to the clister

# This first "run.py" script initializes the cluster, interactively reads the
# configuration and saves it in JSON format to a fixed, well known location in $PWD
# hidden  under .config.json

#load environment variables
import sys
import os
import requests
import json

sys.path.append(os.getcwd()+'/src') 	#Add the ./src directory to path for importing
from env import *			#environment variables and constants, messages, etc.
from src.helpers import *				#helper functions in separate module helpers.py

if __name__ == "__main__":

	config = get_config( env.CONFIG_FILE )

	delete_local_buffer( DATA_DIR )

	#login menu loop
	config_is_ok = 'n'
	while not ( config_is_ok.lower() == 'y' ):

		display_login_menu( config )
		config_is_ok = get_input( message=env.MSG_IS_OK, valid_options= env.yYnN )
		if ( config_is_ok.lower()  == 'n'):

			option = get_input( message=env.MSG_ENTER_PARAM_CHANGE, valid_options=env.hotkeys_login.keys() )
			value = get_input( message=env.MSG_ENTER_NEW_VALUE ) #valid_options=ANY
			config[hotkeys_login[option]] = value
	#TODO: LOGIN TO CLUSTER USING CREDENTIALS
	if not login_to_cluster( config ):
		log(
			log_level='ERROR',
			operation='LOGIN',
			objects=['config'],
			indx=0,
			content=''
			)
		sys.exit()
	
	#main menu loop
	option = '1' 									#initialize to anything different than 'EXIT'
	while env.hotkeys_main[option] is not 'EXIT':

		display_main_menu( config, env.state )
		option = get_input( message=env.MSG_ENTER_CMD, valid_options=env.hotkeys_main.keys() )
		message = 'MSG_'+(env.hotkeys_main[ option ]).upper
		
		#get the name of the function to be executed from the menu hotkeys
		func = env.hotkeys_main.get( option, 'noop' ) #default is noop
		
		#execute the primary function selected with "option" (get_users, get_groups, get_acls)
		#result will be a dictionary of the users, groups, acls, etc.
		func_result = func( config['DCOS_IP'], config['DATA_DIR'] )
		
		#execute secondary function associated with the primary if it exists
		#(get_users_groups, get_groups_users, get_permissions_actions)
		if func in env.secondary_functions.keys():
			sec_func = env.secondary_functions.get( func.__name__, 'noop' )
			sec_result = sec_func( config['DCOS_IP'], config['DATA_DIR'], func_result )

	#Exit
	log(
		log_level='INFO',
		operation='EXIT',
		objects=['Program'],
		indx=0,
		content='* DONE *'
		)
	sys.exit(1)
