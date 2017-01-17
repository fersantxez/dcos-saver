#!/usr/bin/env python3
#
# helpers.py: helper functions for other processes in the project to use
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Set of functions repeatedly used in other parts of this project. 
# Put on a separate module for clarity and readability.

import os
import json
import sys
from shutil import copy2
from ntpath import basename
import requests
import getpass
#sub-modules
import env
from get_users import *
from get_groups import *
from get_acls import *
from get_ldap import *
from get_agents import *
from get_service_groups import *
from post_users import *
from post_groups import *
from post_acls import *
from post_ldap import *
from post_service_groups import *

def clear_screen():
	"""
	Clear the screen.
	"""
	os.system('clear')

	return True


def log ( log_level, operation, objects, indx, content ):
	"""
	Log to stdout (and potentially any other log sink) a message with the right format.
	Returns True.
	"""

	if not ( log_level in env.log_levels ):
		log( 'ERROR', 0, env.ERROR_UNKNOWN_LOG_LEVEL )
		return False

	#INFO messages do not create a new line
	if not ( log_level == 'INFO'):
		line_start = '\n'
	else:
		line_start = ''

	if not ( log_level == 'INFO'):
		line_end = '\n'
	else:
		line_end = '\r'
	#print log message with the right format. Fixed field lengths for justification
	print( '{0}{1:<3} {2:<5}: {3:<4} {4:<3}: {5}: {6}'.format(
			line_start,		#0
			env.MARK,		#1
			log_level,		#2
			operation,		#3
			indx,			#4
			', '.join( str(x) for x in objects ),			#5
			content			#6
			),
		end=line_end,
		flush=not bool( log_level=='INFO' )
		)

	return True

def get_input ( message, valid_options=[] ):
	"""
	Ask the user to enter an option, validate is a valid option from the valid_options. Loops until a valid option is entered.
	Returns the entered option. ( TODO: or ''?/False? if cancelled. )
	If valid_options is not passed, this is used to enter a value and not an option (any value is valid).
	"""

	while True:
		print('{0} {1}: '.format( env.MARK_INPUT, message ) )
		user_input = input( env.MSG_ENTER_NEW_VALUE )
		if ( ( valid_options == [] ) or ( user_input in valid_options ) ):
			return user_input
		else:
			log(
				log_level='ERROR',
				operation='INPUT',
				objects=['INPUT'],
				indx=0,
				content=env.ERROR_INVALID_OPTION
				)

def create_config ( config_path ) :
	"""
	Create a new full program configuration from defaults and return a dictionary with 
	all its parameters. Program configuration is stored in raw JSON so we just need
	to load it from the defaults in "env" and use standard `json` to parse it into a dictionary.
	Returns config as a dictionary.
	"""

	if os.path.exists ( config_path ):
		log(
			log_level='ERROR',
			operation='CREATE',
			objects=['Config'],
			indx=0,
			content=config_path+' exists.'
			)
		return False
	#create a config dictionary and add the values in "env"
	config={
		'DCOS_IP': env.DCOS_IP, 
		'DCOS_USERNAME': env.DCOS_USERNAME, 
		'DCOS_PASSWORD': env.DCOS_PASSWORD, 
		'DEFAULT_USER_PASSWORD': env.DEFAULT_USER_PASSWORD, 
		'DEFAULT_USER_SECRET': env.DEFAULT_USER_SECRET, 
		'WORKING_DIR': env.WORKING_DIR, 
		'CONFIG_FILE': env.CONFIG_FILE, 
		'USERS_FILE': env.USERS_FILE, 
		'USERS_GROUPS_FILE': env.USERS_GROUPS_FILE, 
		'GROUPS_FILE': env.GROUPS_FILE, 
		'GROUPS_USERS_FILE': env.GROUPS_USERS_FILE, 
		'ACLS_FILE': env.ACLS_FILE, 
		'ACLS_PERMISSIONS_FILE': env.ACLS_PERMISSIONS_FILE, 
		'AGENTS_FILE': env.AGENTS_FILE,
		'SERVICE_GROUPS_FILE': env.SERVICE_GROUPS_FILE,
		'TOKEN': ''
	}
	config_file = open( config_path, 'w' )  	#open the config file for writing
	config_file.write( json.dumps( config ) )	#read the entire file into a dict with JSON format
	config_file.close()

	get_input( message=env.MSG_PRESS_ENTER )
	
	return config

def get_config ( config_path ) :
	"""
	Get the full program configuration from the file and return a dictionary with 
	all its parameters. Program configuration is stored in raw JSON so we just need
	to load it and use standard `json` to parse it into a dictionary.
	Returns config as a dictionary.
	"""

	if not os.path.exists ( config_path ):
		log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Config'],
			indx=0,
			content=config_path
			)
		return False
	config_file = open( config_path, 'r' )  	#open the config file for reading
	read_config = config_file.read()			#read the entire file into a dict with JSON format
	config_file.close()
	config = dict( json.loads( read_config ) )	#parse read config as JSON into readable dictionary
	
	return config

def show_config ( DCOS_IP=None ) :
	"""
	Show the full program configuration from the file.
	Program configuration is received as a dictionary.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""

	config = get_config( env.CONFIG_FILE )
	print('{0}'.format( env.MSG_CURRENT_CONFIG ) )
	print('{0} : {1}'.format( env.MSG_DCOS_IP, config['DCOS_IP'] ) ) 
	print('{0} : {1}'.format( env.MSG_DCOS_USERNAME, config['DCOS_USERNAME'] ) )
	print('{0} : {1}'.format( env.MSG_DCOS_PASSWORD, '*'*len(config['DCOS_PASSWORD']) ) )
	print('{0} : {1}'.format( env.MSG_DEFAULT_PASSWORD, '*'*len(config['DEFAULT_USER_PASSWORD']) ) )
	print('{0} : {1}'.format( env.MSG_TOKEN, config['TOKEN'] ) )	
	get_input( message=env.MSG_PRESS_ENTER )

	return True

def update_config ( config_path, config ) :
	"""
	Updates the configuration saved on disk with the values passed on as argument.
	"""

	if not os.path.exists ( config_path ):
		log(
			log_level='ERROR',
			operation='_UPDATE',
			objects=['Config'],
			indx=0,
			content=config_path
			)
		return False
	#create a config dictionary and add the values in "env"
	old_config = get_config( config_path )
	old_config.update( config )
	config_file = open( config_path, 'w' )  	#open the config file for writing
	config_file.write( json.dumps( config ) )			#read the entire file into a dict with JSON format
	config_file.close()
	
	return config


def list_configs ( DCOS_IP=None ):
	"""
	List all the DC/OS configurations available on disk to be loaded.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""
	print( '{0}'.format( env.MSG_AVAIL_CONFIGS ) )
	for config_dir in os.listdir( env.BACKUP_DIR ): print ('[{0}]'.format( config_dir ) )
	get_input( message=env.MSG_PRESS_ENTER )

	return True

def load_configs ( DCOS_IP=None ):
	"""
	Load a DC/OS configuration from disk into local buffer. If the local buffer directory does not exist, create it.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""

	#create the DATA_DIR if it doesn't exist yet
	if not os.path.isdir( env.DATA_DIR ):
		os.makedirs( env.DATA_DIR )
	list_configs()
	name = get_input( message=env.MSG_ENTER_CONFIG_LOAD )
	if os.path.exists( env.BACKUP_DIR+'/'+name ):
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_FILE ), 			env.DATA_DIR+'/'+basename( env.USERS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_GROUPS_FILE ), 		env.DATA_DIR+'/'+basename( env.USERS_GROUPS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_FILE ), 		env.DATA_DIR+'/'+basename( env.GROUPS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_USERS_FILE ), 		env.DATA_DIR+'/'+basename( env.GROUPS_USERS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_FILE ), 			env.DATA_DIR+'/'+basename( env.ACLS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_PERMISSIONS_FILE ),	env.DATA_DIR+'/'+basename( env.ACLS_PERMISSIONS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.AGENTS_FILE ),	env.DATA_DIR+'/'+basename( env.AGENTS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.SERVICE_GROUPS_FILE ),	env.DATA_DIR+'/'+basename( env.SERVICE_GROUPS_FILE )  )

		get_input( message=env.MSG_PRESS_ENTER )
		return True
	else:
		log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Config'],
			indx=0,
			content=env.ERROR_CONFIG_NOT_FOUND
			)
		return False

def save_configs ( DCOS_IP=None ):
	"""
	Save the running DC/OS configuration to disk from local buffer.
	"""
	list_configs( config )
	name = get_input( message=env.MSG_ENTER_CONFIG_SAVE )
	if not os.path.exists( env.BACKUP_DIR+'/'+name ):
		os.makedirs( env.BACKUP_DIR+'/'+name)
	copy2( env.DATA_DIR+'/'+basename( env.USERS_FILE ), 		env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.USERS_GROUPS_FILE ), 	env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_GROUPS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.GROUPS_FILE ), 		env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.GROUPS_USERS_FILE ),  	env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_USERS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.ACLS_FILE ), 		env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.ACLS_PERMISSIONS_FILE ),	env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_PERMISSIONS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.AGENTS_FILE ),	env.BACKUP_DIR+'/'+name+'/'+basename( env.AGENTS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.SERVICE_GROUPS_FILE ),	env.BACKUP_DIR+'/'+name+'/'+basename( env.SERVICE_GROUPS_FILE ) )

	get_input( message=env.MSG_PRESS_ENTER )

	return True

def check_users ( DCOS_IP=None ):
	"""
	List all the users currently in the application's buffer.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""

	config = helpers.get_config( env.CONFIG_FILE )  
	print('{0}'.format( env.MSG_CURRENT_USERS ) )
	#Open users file
	try:  
		users_file = open( env.USERS_FILE, 'r' )  
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Users'],
			indx=0,
			content=env.MSG_ERROR_NO_USERS
			)
		get_input( message=env.MSG_PRESS_ENTER )
		return False #return Error if file isn't available
    #load entire text file and convert to JSON - dictionary
	users = json.loads( users_file.read() )
	users_file.close()

	for index, user in ( enumerate( users['array'] ) ):
		print( 'User #{0}: {1}'.format(index, user['uid'] ) )

	#open up the users_groups file and print the groups each user is a member of
	try:  
		users_groups_file = open( env.USERS_GROUPS_FILE, 'r' ) 
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Users', 'Groups'],
			indx=0,
			content=request.text
			)
		get_input( message=env.MSG_PRESS_ENTER )
		return False #return Error if file isn't available
    #load entire text file and convert to JSON - dictionary
	users_groups = json.loads( users_groups_file.read() )
	users_groups_file.close()	

	for index, user_group in ( enumerate( users_groups['array'] ) ):

		groups = user_group['groups']

		for group in groups:

			print( 'User {0} belongs to Group: {1}'.format(user_group['uid'], group['group']['gid'] ) )

	get_input( message=env.MSG_PRESS_ENTER )

	return True

def check_groups ( DCOS_IP=None ):
	"""
	List all the groups currently in the application's buffer.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""

	config = helpers.get_config( env.CONFIG_FILE )  
	print('{0}'.format( env.MSG_CURRENT_GROUPS ) )
	#Open groups file
	try:  
		groups_file = open( env.GROUPS_FILE, 'r' ) 
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Groups'],
			indx=0,
			content=env.MSG_ERROR_NO_GROUPS
			)
		get_input( message=env.MSG_PRESS_ENTER )
		return False #return Error if file isn't available
    #load entire text file and convert to JSON - dictionary
	groups = json.loads( groups_file.read() )
	groups_file.close()

	for index, group in ( enumerate( groups['array'] ) ):
		print( 'Group #{0}: {1}'.format(index, group['gid'] ) )

	#open up the groups_users file and print the users each group has as members
	try:  
		groups_users_file = open( env.GROUPS_USERS_FILE, 'r' ) 
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['Groups', 'Users'],
			indx=0,
			content=request.text
			)
		get_input( message=env.MSG_PRESS_ENTER )
		return False #return Error if file isn't available
    #load entire text file and convert to JSON - dictionary
	groups_users = json.loads( groups_users_file.read() )
	groups_users_file.close()	

	#loop through the list of users_groups and print them
	for index, group_user in ( enumerate( groups_users['array'] ) ):

		users = group_user['users']

		for user in users:

			print( 'Group {0} has as a member User: {1}'.format(group_user['gid'], user['user']['uid'] ) )


	get_input( message=env.MSG_PRESS_ENTER )

	return True

def check_acls ( DCOS_IP=None ):
	"""
	List all the ACLs currently in the application's buffer.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""

	config = helpers.get_config( env.CONFIG_FILE )  
	print('{0}'.format( env.MSG_CURRENT_ACLS ) )
	#Open users file
	try:  
		#open the groups file and load the LIST of Groups from JSON
		acls_file = open( env.ACLS_FILE, 'r' )   
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['ACLs'],
			indx=0,
			content=env.MSG_ERROR_NO_ACLS
			)
		get_input( message=env.MSG_PRESS_ENTER )
		return False #return Error if file isn't available
    #load entire text file and convert to JSON - dictionary
	acls = json.loads( acls_file.read() )
	acls_file.close()

	#loop through the list of groups and
	for index, acl in ( enumerate( acls['array'] ) ):
		print( 'ACL #{0}: {1}'.format(index, acl['rid'] ) )

	get_input( message=env.MSG_PRESS_ENTER )

	return True 

def check_ldap ( DCOS_IP=None ):
	"""
	List the LDAP configuration currently in the application's buffer.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""

	config = helpers.get_config( env.CONFIG_FILE )  
	print('{0}'.format( env.MSG_CURRENT_LDAP ) )
	#Open users file
	try:  
		#open the groups file and load the LIST of Groups from JSON
		ldap_file = open( env.LDAP_FILE, 'r' )   
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['LDAP'],
			indx=0,
			content=env.MSG_ERROR_NO_LDAP
			)
		get_input( message=env.MSG_PRESS_ENTER )
		return False #return Error if file isn't available
    #load entire text file and convert to JSON - dictionary
	ldap = json.loads( ldap_file.read() )
	ldap_file.close()

	print( 'LDAP Configuration: {1}'.format(ldap ) )

	get_input( message=env.MSG_PRESS_ENTER )

	return True 

def check_service_groups ( DCOS_IP=None ):
	"""
	List all the Service Groups currently in the application's buffer.
	Takes no parameters but DCOS_IP is left to use the same interface on all options.
	"""

	config = helpers.get_config( env.CONFIG_FILE )  
	print('{0}'.format( env.MSG_CURRENT_SERVICE_GROUPS ) )
	try:  
		#open the service groups file and load the LIST of Service Groups from JSON
		service_groups_file = open( env.SERVICE_GROUPS_FILE, 'r' )   
	except IOError as error:
		helpers.log(
			log_level='ERROR',
			operation='LOAD',
			objects=['ACLs'],
			indx=0,
			content=env.MSG_ERROR_NO_SERVICE_GROUPS
			)
		get_input( message=env.MSG_PRESS_ENTER )
		return False #return Error if file isn't available
    #load entire text file and convert to JSON - dictionary
	service_groups = json.loads( service_groups_file.read() )
	service_groups_file.close()

	walk_and_print ( service_groups, "Service Groups" )

	get_input( message=env.MSG_PRESS_ENTER )

	return True 

def delete_local_buffer ( path ) :
	"""
	Delete the local buffer that stores the temporary configuration.
	"""
	#check whether the directory exists
	if os.path.isdir( path ):
		for root, dirs, files in os.walk( path, topdown=False ):
			for name in files:
				os.remove( os.path.join( root, name ) )
			for name in dirs:
				os.rmdir( os.path.join( root, name ) )
		os.rmdir( path )
	else:
		log(
			log_level='ERROR',
			operation='_DELETE',
			objects=['Local_buffer'],
			indx=0,
			content=env.ERROR_BUFFER_NOT_FOUND
			)

	return True

def create_new_local_buffer ( path ) :
	"""
	Create a brand new local buffer that stores the temporary configuration.
	"""
	#check whether the buffer directory exists, delete if so.
	if os.path.isdir( path ):
		for root, dirs, files in os.walk( path, topdown=False ):
			for name in files:
				os.remove( os.path.join( root, name ) )
			for name in dirs:
				os.rmdir( os.path.join( root, name ) )
		os.rmdir( path )

	#create a new local buffer
	os.mkdir( path )

	return True

def menu_line (hotkey='', message='', config_param='', state_param=''):
	""" 
	Format a menu string to the adequate length and justification.
	If a hotkey is provided, print it at the beginning.
	If a config value is provided, print it at the end.
	If state is provided, print at the very end.
	If no message provided, print a full separation line.
	Returns True.
	"""
	if not ( hotkey == '' ):
		print( '{0} '.format( hotkey ), end='', flush=False )
		print( '{0} '.format( ':' ), end='', flush=False )

	if ( message == '' ):
		print( '*'*env.MENU_WIDTH ) #A separation line
	else:
		print( '{0}'.format( message, end='' ) 
			#'*'*int( (env.MENU_WIDTH)-( len(message)+len(config_param) ) ),
			
		)

	if not (config_param == ''):
		print( '{0}'.format( config_param ), end='', flush=False  )

	if not (state_param == ''):
		print( '{0}'.format( state_param ), end='', flush=False  )

	print('')

	return True

def display_login_menu( config ):
	"""
	Display the initial login menu until the user says config is ok. 
	Use the "hotkeys_main" and the login menu messages from "env".
	Display the configuration parameters received as parameter.
	Returns (1) when the user acknowledges that the configuration is_ok.
	"""

	hk = dict( zip( env.hotkeys_login.values(), env.hotkeys_login.keys() ) )	#invert keys and values in dictionary to index by key name

	clear_screen()
	menu_line()
	menu_line( message=env.MSG_APP_TITLE )
	menu_line()
	menu_line( message=env.MSG_CURRENT_CONFIG )
	menu_line()
	menu_line( hotkey=hk['DCOS_IP'], message=env.MSG_DCOS_IP, config_param=config['DCOS_IP'] )
	menu_line()
	menu_line( hotkey=hk['DCOS_USERNAME'], message=env.MSG_DCOS_USERNAME, config_param=config['DCOS_USERNAME'] )
	menu_line()	
	menu_line( hotkey=hk['DCOS_PASSWORD'], message=env.MSG_DCOS_PASSWORD, config_param='*'*len(config['DCOS_PASSWORD']) )
	menu_line()	
	menu_line( hotkey=hk['DEFAULT_USER_PASSWORD'], message=env.MSG_DEFAULT_PASSWORD, config_param='*'*len(config['DEFAULT_USER_PASSWORD']) )
	menu_line()	

	return True


def display_main_menu( config, state ):
	"""
	Display the main app menu until the user chooses the "exit" option. 
	Use the "hotkeys_main" and the login menu messages from "env".
	Display the configuration parameters received as parameter.
	Display the state received as parameter.
	Returns (True) when the user decides to exit.
	"""

	hk = dict( zip( env.hotkeys_main.values(), env.hotkeys_main.keys() ) )	#invert keys and values in dictionary to index by key name

	clear_screen()

	menu_line()
	menu_line( message=env.MSG_APP_TITLE )
	menu_line()
	menu_line( message=env.MSG_AVAIL_CMD )
	menu_line( hotkey=hk['list_configs'], message=env.MSG_LIST_CONFIG )
	menu_line( hotkey=hk['load_configs'], message=env.MSG_LOAD_CONFIG )
	menu_line( hotkey=hk['save_configs'], message=env.MSG_SAVE_CONFIG )
	menu_line( hotkey=hk['show_config'], message=env.MSG_SHOW_CONFIG )	
	menu_line()
	menu_line( message=env.MSG_GET_MENU )
	menu_line( hotkey=hk['get_users'], message=env.MSG_GET_USERS )
	menu_line( hotkey=hk['get_groups'], message=env.MSG_GET_GROUPS )
	menu_line( hotkey=hk['get_acls'], message=env.MSG_GET_ACLS )
	menu_line( hotkey=hk['get_ldap'], message=env.MSG_GET_LDAP )
	menu_line( hotkey=hk['get_agents'], message=env.MSG_GET_AGENTS )
	menu_line( hotkey=hk['get_service_groups'], message=env.MSG_GET_SERVICE_GROUPS )
	menu_line( hotkey=hk['get_all'], message=env.MSG_GET_ALL )
	menu_line()
	menu_line( message=env.MSG_PUT_MENU )
	menu_line( hotkey=hk['post_users'], message=env.MSG_PUT_USERS )
	menu_line( hotkey=hk['post_groups'], message=env.MSG_PUT_GROUPS )
	menu_line( hotkey=hk['post_acls'], message=env.MSG_PUT_ACLS )
	menu_line( hotkey=hk['post_ldap'], message=env.MSG_PUT_LDAP )
	menu_line( hotkey=hk['post_service_groups'], message=env.MSG_PUT_SERVICE_GROUPS )
	menu_line( hotkey=hk['post_all'], message=env.MSG_PUT_ALL )
	menu_line()
	menu_line( message=env.MSG_CHECK_MENU )
	menu_line( hotkey=hk['check_users'], message=env.MSG_CHECK_USERS )
	menu_line( hotkey=hk['check_groups'], message=env.MSG_CHECK_GROUPS )
	menu_line( hotkey=hk['check_acls'], message=env.MSG_CHECK_ACLS )
	menu_line( hotkey=hk['check_ldap'], message=env.MSG_CHECK_LDAP )
	menu_line( hotkey=hk['check_service_groups'], message=env.MSG_CHECK_SERVICE_GROUPS )	
	menu_line()
	menu_line( hotkey=hk['exit'], message=env.MSG_EXIT )		
	menu_line()
	menu_line()

	return True

def noop():
	"""
	No Op.
	"""
	pass

	return True

def escape ( a_string ) :
	"""
	Escape characters that create issues for URLs
	"""
	escaped = a_string.replace("/", "%252F")

	return escaped

def login_to_cluster ( config ):
	"""
	Log into the cluster whose DCOS_IP is specified in 'config' in order to get a valid token, using the username and password in 'config'. Also save the updated token to the config file.
	"""

	api_endpoint = '/acs/api/v1/auth/login'
	url = 'http://'+config['DCOS_IP']+api_endpoint
	headers = {
		'Content-type': 'application/json'
	}
	data = { 
		"uid":		config['DCOS_USERNAME'],
		"password":	config['DCOS_PASSWORD']
		}

	try:
		request = requests.post(
			url,
			data = json.dumps( data ),
			headers=headers
			)
		request.raise_for_status()
		log(
			log_level='INFO',
			operation='GET',
			objects=[request.json],
			indx=0,
			content=request.status_code
			)
	except ( requests.exceptions.HTTPError, requests.exceptions.ConnectionError ) as error:
		log(
			log_level='ERROR',
			operation='GET',
			objects=[config],
			indx=0,
			content=request.text
			)
		return False

	#update the configuration with the newly acquired Token
	config['TOKEN'] = request.json()['token']
	update_config( env.CONFIG_FILE, config )

	return True

def walk_and_print( item, name ):
	"""
	Walks a recursive tree-like structure for items printing them.
	Structure is assumed to have children under 'groups' and name under 'id'
	Receives the tree item and an 'id' as a name to identify each node.
	"""
	if item['groups']:
		for i in item['groups']:
			walk_and_print( i, name )
	else:
		print( "{0}: {1}".format( name, item['id'] ) )

	return True

def format_service_group( service_group ):
	"""
	Walks a (potentially recursive tree-like structure of) service group in a dict that potentially include apps.
	Removes fields that can't be posted initially from the service group:
	- apps (empty it)
	- version (remove it)
	Changes the format of the "id" field to remove "/"
	Modifies the object passed as a parameter, does NOT return.
	"""

	#remove my children's apps
	for index,group in enumerate( service_group['groups'] ):
		#if isinstance( group, list ):
		format_service_group( group )
	
	#remove my own apps
	service_group['apps'] = [] #apps is an empty list
	del service_group['version']

	return True

def exit( DCOS_IP ):
	"""
	Placeholder for operations that need to be done on exit.
	"""

	delete_local_buffer( env.DATA_DIR )
	#Exit
	log(
		log_level='INFO',
		operation='EXIT',
		objects=['Program'],
		indx=0,
		content=env.MSG_DONE
		)
	sys.exit(1)

	return None

def get_all( DCOS_IP ):
	"""
	Do a full GET of all parameters supported. Simply calls other functions."
	"""

	get_users( DCOS_IP )
	get_groups( DCOS_IP )
	get_acls( DCOS_IP )
	get_ldap( DCOS_IP )
	get_service_groups( DCOS_IP )
	get_agents( DCOS_IP )

	return True

def post_all( DCOS_IP ):
	"""
	Do a full GET of all parameters supported. Simply calls other functions."
	"""

	post_users( DCOS_IP )
	post_groups( DCOS_IP )
	post_acls( DCOS_IP )
	post_service_groups( DCOS_IP )
	post_ldap( DCOS_IP )

	return True
