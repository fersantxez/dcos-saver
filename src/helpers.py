#!/usr/bin/env python
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
import env

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
	sys.stdout.write( '{0}{1:<3} {2:<5}: {3:<4} {4:<3}: {5:30}: {6:>20} {7:>1}'.format(
			line_start,		#0
			env.MARK,			#1
			log_level,		#2
			operation,		#3
			indx,			#4
			', '.join( str(x) for x in objects ),			#5
			content,		#6
			line_end		#7
			)
		)
	#return carriage for repeatig line if 'INFO'
	if ( log_level == 'INFO' ):
		sys.stdout.flush()
	return True

def get_input ( message, valid_options=[] ):
	"""
	Ask the user to enter an option, validate is a valid option from the valid_options. Loops until a valid option is entered.
	Returns the entered option. ( TODO: or ''?/False? if cancelled. )
	If valid_options is not passed, this is used to enter a value and not an option (any value is valid).
	"""

	while True:
		sys.stdout.write('{0} {1}: \n'.format( env.MARK_INPUT, message ) )
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

def get_config ( config_path ) :
	"""
	Get the full program configuration from the file and returns a dictionary with 
	all its parameters. Program configuration is stored in raw JSON so we just need
	to load it and use standard `json` to parse it into a dictionary.
	Returns config as a dictionary.
	"""

	config_file = open( config_path, 'r' )  	#open the config file for reading
	read_config = config_file.read()			#read the entire file into a dict with JSON format
	config_file.close()
	config = dict( json.loads( read_config ) )		#parse read config as JSON into readable dictionary

	return config

def show_config ( config ) :
	"""
	Show the full program configuration from the file.
	Program configuration is received as a dictionary.
	"""

	sys.stdout.write( '{} \n'.format( env.MSG_CURRENT_CONFIG ) )
	sys.stdout.write( '{} : {} \n'.format( env.MSG_DCOS_IP, config['DCOS_IP'] ) ) 
	sys.stdout.write( '{} : {} \n'.format( env.MSG_DCOS_USERNAME, config['USERNAME'] ) )
	sys.stdout.write( '{} : {} \n'.format( env.MSG_DCOS_PW, config['PASSWORD'] ) )
	sys.stdout.write( '{} : {} \n'.format( env.MSG_DEFAULT_PW, config['DEFAULT_USER_PASSWORD'] ) )

	return True

def list_config ( config ):
	"""
	List all the DC/OS configurations available on disk to be loaded.
	"""
	sys.stdout.write( '{} \n'.format( env.MSG_AVAIL_CONFIGS ) )
	for config_dir in os.listdir( env.BACKUP_DIR ): print( config_dir )

	return True

def load_config ( config ):
	"""
	Load a DC/OS configuration from disk into local buffer. If the local buffer directory does not exist, create it.
	"""

	if not os.path.exists( env.DATA_DIR ):
		os.makedirs( env.DATA_DIR )
	list_config( config )
	name = get_input( message=env.MSG_ENTER_CONFIG_LOAD )
	if os.path.exists( env.BACKUP_DIR+'/'+name ):
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_FILE ), 			env.DATA_DIR+'/'+basename( env.USERS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_GROUPS_FILE ), 		env.DATA_DIR+'/'+basename( env.USERS_GROUPS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_FILE ), 		env.DATA_DIR+'/'+basename( env.GROUPS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_USERS_FILE ), 		env.DATA_DIR+'/'+basename( env.GROUPS_USERS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_FILE ), 			env.DATA_DIR+'/'+basename( env.ACLS_FILE )  )
		copy2( env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_PERMISSIONS_FILE ),	env.DATA_DIR+'/'+basename( env.ACLS_PERMISSIONS_FILE )  )
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

def save_config ( config ):
	"""
	Save the running DC/OS configuration to disk from local buffer.
	"""
	list_config( config )
	name = get_input( message=env.MSG_ENTER_CONFIG_SAVE )
	if not os.path.exists( env.BACKUP_DIR+'/'+name ):
		os.makedirs( env.BACKUP_DIR+'/'+name)
	copy2( env.DATA_DIR+'/'+basename( env.USERS_FILE ), 		env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.USERS_GROUPS_FILE ), 	env.BACKUP_DIR+'/'+name+'/'+basename( env.USERS_GROUPS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.GROUPS_FILE ), 		env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.GROUPS_USERS_FILE ),  	env.BACKUP_DIR+'/'+name+'/'+basename( env.GROUPS_USERS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.ACLS_FILE ), 		env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_FILE ) )
	copy2( env.DATA_DIR+'/'+basename( env.ACLS_PERMISSIONS_FILE ),	env.BACKUP_DIR+'/'+name+'/'+basename( env.ACLS_PERMISSIONS_FILE ) )

	return True


def delete_local_buffer ( path ) :
	"""
	Delete the local buffer that stores the temporary configuration.
	"""
	if os.path.exists( path ):
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
		sys.stdout.write('{0}'.format( hotkey ) )

	if ( message == '' ):
		sys.stdout.write('*'*env.MENU_WIDTH + '\n') #A separation line
	else:
		sys.stdout.write( '{0} {1} {2}'.format( 
				'*'*int( ( env.MENU_WIDTH-len( message ) )/2 ),
				message,	
				'*'*int( ( env.MENU_WIDTH-len( message ) )/2 )
				)
			)

	if not (config_param == ''):
		sys.stdout.write('{0}'.format( config_param ) )

	if not (state_param == ''):
		sys.stdout.write('{0}'.format( state_param ) )

	sys.stdout.write('\n')

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
	menu_line( hotkey=hk['DCOS_USERNAME'], message=env.MSG_DCOS_USERNAME, config_param=config['USERNAME'] )
	menu_line()	
	menu_line( hotkey=hk['PASSWORD'], message=env.MSG_DCOS_PW, config_param=config['PASSWORD'] )
	menu_line()	
	menu_line( hotkey=hk['DEFAULT_USER_PASSWORD'], message=env.MSG_DEFAULT_PW, config_param=config['DEFAULT_USER_PASSWORD'] )
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
	menu_line( hotkey=hk['list_config'], message=env.MSG_LIST_CONFIG )
	menu_line( hotkey=hk['load_config'], message=env.MSG_LOAD_CONFIG )
	menu_line( hotkey=hk['save_config'], message=env.MSG_SAVE_CONFIG )
	menu_line( hotkey=hk['show_config'], message=env.MSG_SHOW_CONFIG )	
	menu_line()
	menu_line( message=env.MSG_GET_MENU )
	menu_line( hotkey=hk['get_users'], message=env.MSG_GET_USERS )
	menu_line( hotkey=hk['get_groups'], message=env.MSG_GET_GROUPS )
	menu_line( hotkey=hk['get_acls'], message=env.MSG_GET_ACLS )
	menu_line( hotkey=hk['get_all'], message=env.MSG_GET_ALL )
	menu_line()
	menu_line( message=env.MSG_PUT_MENU )
	menu_line( hotkey=hk['put_users'], message=env.MSG_PUT_USERS )
	menu_line( hotkey=hk['put_groups'], message=env.MSG_PUT_GROUPS )
	menu_line( hotkey=hk['put_acls'], message=env.MSG_PUT_ACLS )
	menu_line( hotkey=hk['put_all'], message=env.MSG_PUT_ALL )
	menu_line()
	menu_line( message=env.MSG_CHECK_MENU )
	menu_line( hotkey=hk['check_users'], message=env.MSG_CHECK_USERS )
	menu_line( hotkey=hk['check_groups'], message=env.MSG_CHECK_GROUPS )
	menu_line( hotkey=hk['check_acls'], message=env.MSG_CHECK_ACLS )
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


