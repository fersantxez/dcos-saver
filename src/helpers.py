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
import env

# FUNCTION get_conf
def get_config ( config_path ) :
	"""
	Get the full program configuration from the file and returns a dictionary with 
	all its parameters. Program configuration is stored in raw JSON so we just need
	to load it and use standard `json` to parse it into a dictionary.
	Returns config as a dictionary
	"""

	config_file = open( config_path, 'r' )  	#open the config file for reading
	read_config = config_file.read()			#read the entire file into a dict with JSON format
	config_file.close()
	config = json.loads( read_config )			#parse read config as JSON into readable dictionary

	return config

def log ( string log_level, string operation, 
	string obj_0, string obj_1, string obj_2, string obj_3, string obj_4,
	int indx, string content ):
	"""
	Log to stdout (and potentially any other log sink) a message with the right format.
	Returns True.
	"""

	if not (log_level in log_levels):
		log( 'ERROR', 0, ERROR_UNKNOWN_LOG_LEVEL )

	#INFO messages do not create a new line
	if not ( log_level == 'INFO'):
		line_start = '\n'
	else
		line_start = ''

	if not ( log_level == 'INFO'):
		line_end = '\n'
	else
		line_end = '\r'
	#print log message with the right format. Fixed field lengths for justification
	sys.stdout.write( '{0:<1} {1:<3} (2:<5): {3:<4} {4:<3}: {5:<10}: {6:<10}: {7:<10}: {8:<10}: {9:<10}: {10:>20} {7:>11}'.format(
			line_start,		#0
			mark,			#1
			log_level,		#2
			operation,		#3
			indx,			#4
			obj_0,			#5
			obj_1,			#6
			obj_2,			#7
			obj_3,			#8
			opj_4,			#9
			content,			#10
			line_end		#11
			)
		)
	#return carriage for repeatig line if 'INFO'
	if ( log_level == 'INFO' ):
		sys.stdout.flush()
	return True

def clear_screen( ):
	"""
	Clear the screen.
	Returns True
	"""

	#TODO:

	return True

def menu_line (string hotkey, string message, string config_param, string state_param):
	""" 
	Format a menu string to the adequate length and justification.
	If a hotkey is provided, print it at the beginning.
	If a config value is provided, print it at the end.
	If state is provided, print at the very end.
	If no message provided, print a full separation line.
	Returns True
	"""
	if not ( hotkey == None ):
		sys.stdout.write('{0}'.format( hotkey ) )

	if ( message == None ):
		sys.stdout.write('*'*MENU_WIDTH + '\n') #A separation line
	else:
		sys.stdout.write( '{1} {2} {3} {4}'.format( 
				'*'*( ( MENU_WIDTH-len( message ) )/2 ),
				message,	
				'*'*( ( MENU_WIDTH-len( message )/2 ) ),
				':'
				)
			)

	if not (config_param == None):
		sys.stdout.write('{0}'.format( config_param ) )

	if not (state_param == None):
		sys.stdout.write('{0}'.format( state_param ) )

	return True

def get_input ( string message, list valid_options ):
	"""
	Ask the user to enter an option, validate is a valid option from the valid_optionss. Loops until a valid option is entered.
	Returns the entered option. ( TODO: or ''?/False? if cancelled. )
	"""

	while True:
		sys.stdout.write('{0} {1}: '.format( mark_input, message ) )
		input( user_input )
		if (user_input in valid_options):
			return user_input
		else
			log(
				log_level='ERROR',
				operation='INPUT',
				obj_0='INPUT',
				indx=0,
				content=ERROR_INVALID_OPTION
				)
		return input


def display_login_menu( dict config ):
	"""
	Display the initial login menu until the user says config is ok. 
	Use the "hotkeys_main" and the login menu messages from "env".
	Display the configuration parameters received as parameter.
	Returns (1) when the user acknowledges that the configuration is_ok.
	"""

	hk = hotkeys_login	#brief notation
	is_ok = false

	while ( is_ok == false ):
		clear_screen()
		menu_line()
		menu_line( message=MSG_APP_TITLE )
		menu_line()
		menu_line( message=MSG_CURRENT_CONFIG )
		menu_line()
		menu_line( hotkey=hk['KEY_DCOS_IP'], message=MSG_DCOS_IP, config_param=config['DCOS_IP'] )
		menu_line()
		menu_line( hotkey=hk['KEY_DCOS_USERNAME'], message=MSG_DCOS_USERNAME, config_param=config['USERNAME'] )
		menu_line()	
		menu_line( hotkey=hk['KEY_DCOS_PW'], message=MSG_DCOS_PW, config_param=config['PASSWORD'] )
		menu_line()	
		menu_line( hotkey=hk['KEY_DEFAULT_PW'], message=MSG_DEFAULT_PW, config_param=config['DEFAULT_PW'] )
		menu_line()	

		is_ok = get_input( message=MSG_IS_OK, options=list( yYnN.keys() ) )
		if is_ok == false:
			get_input( message=MSG_ENTER_PARAM_CHANGE, options=list( hotkeys_login.keys() ) )

	return True


def display_main_menu( dict config, dict state ):
	"""
	Display the main app menu until the user chooses the "exit" option. 
	Use the "hotkeys_main" and the login menu messages from "env".
	Display the configuration parameters received as parameter.
	Display the state received as parameter.
	Returns (True) when the user decides to exit
	"""

	hk = hotkeys_main	#brief notation
	user_input = ''		#start empty

	#print menu and get user input
	while not ( user_input == hk['KEY_EXIT'] ):
		clear_screen()
		menu_line()
		menu_line( message=MSG_APP_TITLE )
		menu_line()
		menu_line( message=MSG_AVAIL_CMD )
		menu_line( hotkey=hk['KEY_LIST_CONFIG'], message=MSG_LIST_CONFIG )
		menu_line( hotkey=hk['KEY_LOAD_CONFIG'], message=MSG_LOAD_CONFIG )
		menu_line( hotkey=hk['KEY_SAVE_CONFIG'], message=MSG_SAVE_CONFIG )	
		menu_line()
		menu_line( message=MSG_GET )
		menu_line( hotkey=hk['KEY_GET_USERS'], message=MSG_GET_USERS )
		menu_line( hotkey=hk['KEY_GET_GROUPS'], message=MSG_GET_GROUPS )
		menu_line( hotkey=hk['KEY_GET_ACLS'], message=MSG_GET_ACLS )
		menu_line( hotkey=hk['KEY_GET_ALL'], message=MSG_GET_ALL )
		menu_line()
		menu_line( message=MSG_PUT )
		menu_line( hotkey=hk['KEY_PUT_USERS'], message=MSG_PUT_USERS )
		menu_line( hotkey=hk['KEY_PUT_GROUPS'], message=MSG_PUT_GROUPS )
		menu_line( hotkey=hk['KEY_PUT_ACLS'], message=MSG_PUT_ACLS )
		menu_line( hotkey=hk['KEY_PUT_ALL'], message=MSG_PUT_ALL )
		menu_line()
		menu_line( message=MSG_CHECK )
		menu_line( hotkey=hk['KEY_CHECK_USERS'], message=MSG_CHECK_USERS )
		menu_line( hotkey=hk['KEY_CHECK_GROUPS'], message=MSG_CHECK_GROUPS )
		menu_line( hotkey=hk['KEY_CHECK_ACLS'], message=MSG_CHECK_ACLS )
		menu_line( hotkey=hk['KEY_CHECK_CONFIG'], message=MSG_CHECK_CONFIG )
		menu_line()
		menu_line( hotkey=hk['KEY_EXIT'], message=MSG_EXIT )		
		menu_line()
		menu_line()
		user_input = get_input( message=MSG_ENTER_CMD, valid_options=hk )

	#TODO: execute on chosen option
	# no case/switch. May require inverting the hotkeys_* dict and name after functions
	# http://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement

	return True


