#!/usr/bin/env python
#
# env.py: environment variables for other processes in the project to use
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#

MENU_WIDTH = 50

#Mark for outputs and inputs
mark = '** '
mark_input = '++ '

#Menu messages
#Login menu
MSG_APP_TITLE 			= 'Mesosphere DC/OS - IAM Config Backup and Restore Utility'
MSG_CURRENT_CONFIG 		= 'Current configuration: '
MSG_DCOS_IP 			= 'DC/OS IP or DNS name: '
MSG_DCOS_USERNAME 		= 'DC/OS username: '
MSG_DCOS_PW		 		= 'DC/OS password: '
MSG_DEFAULT_PW 			= 'Default password for restored users: '
MSG_IS_OK				= 'Is this configuration ok? (y/n): '
MSG_ENTER_PARAM_CHANGE	= 'Enter parameter to change: '
#Main menu
MSG_AVAIL_CMD			= 'Available commands: '
MSG_ENTER_CMD			= 'Enter commmand: '
MSG_LOAD_SAVE			= 'LOAD/SAVE configuration from/to local buffer.'
MSG_LIST_CONFIG			= 'LIST configurations available on disk.'
MSG_LOAD_CONFIG			= 'LOAD a configuration available on disk.'
MSG_SAVE_CONFIG			= 'SAVE current local buffer as configuration to disk.'
MSG_GET					= 'GET configuration from a DC/OS cluster into local buffer.'
MSG_GET_USERS			= 'GET Users from DC/OS cluster.'
MSG_GET_GROUPS			= 'GET Groups from DC/OS cluster.'
MSG_GET_ACLS			= 'GET ACLs from DC/OS cluster.'
MSG_GET_ALL				= 'GET ALL config from DC/OS cluster.'
MSG_PUT					= 'PUT configuration to a DC/OS cluster from local buffer.'
MSG_PUT_USERS			= 'PUT Users to DC/OS cluster.'
MSG_PUT_GROUPS			= 'PUT Groups to DC/OS cluster.'
MSG_PUT_ACLS			= 'PUT ACLs to DC/OS cluster.'
MSG_PUT_ALL				= 'PUT ALL config to DC/OS cluster.'
MSG_CHECK				= 'CHECK current local buffer configuration.'
MSG_CHECK_USERS			= 'CHECK Users in local buffer.'
MSG_CHECK_GROUPS		= 'CHECK Groups in local buffer.'
MSG_CHECK_ACLS			= 'CHECK ACLs in local buffer.'
MSG_CHECK_CONFIG		= 'CHECK Configuration for this application.'
MSG_EXIT				= 'EXIT this application.'

#hotkeys - login menu
hotkeys_login = {
'KEY_DCOS_IP' 		: '1',
'KEY_DCOS_USERNAME'	: '2',
'KEY_DCOS_PW' 		: '3',
'KEY_DEFAULT_PW' 	: '4'
}

#hotkeys - main menu
hotkeys_main = {
'KEY_LIST_CONFIG' 	: 'd',
'KEY_LOAD_CONFIG'	: 'l',
'KEY_SAVE_CONFIG'	: 's',
'KEY_GET_USERS' 	: '1',
'KEY_GET_GROUPS' 	: '2',
'KEY_GET_ACLS' 		: '3',
'KEY_get_GET' 		: 'g',
'KEY_PUT_USERS' 	: '4',
'KEY_PUT_GROUPS' 	: '5',
'KEY_PUT_ALCS' 		: '6',
'KEY_FULL_PUT' 		: 'p',
'KEY_CHECK_USERS' 	: '7',
'KEY_CHECK_GROUPS' 	: '8',
'KEY_CHECK_ACLS' 	: '9',
'KEY_CHECK_CONFIG' 	: '0',
'KEY_EXIT' 			: 'x'
}

# y/n input options
yYnN = {
'y'		: 'y',
'Y'		: 'Y',
'n'		: 'n',
'N'		: 'N',
}

#Error messages
ERROR_CONFIG_NOT_FOUND = 'Configuration not found. Please run ./run.sh first.'
ERROR_EMPTY_BUFFER = 'Buffer is empty. Please LOAD or GET before POSTing.'
ERROR_UNKNOWN_LOG_LEVEL = 'Unknown log level.'
ERROR_INVALID_OPTION = 'Invalid input. Please choose a valid option.'

#Log levels - tuple
log_levels = (
	'INFO',
	'DEBUG',
	'ERROR'
	)

#TODO: translate these to valid Python
#clear screen
CLS 		='printf \033c'
#pretty colours
RED			='\033[0;31m'
BLUE		='\033[1;34m'
GREEN		='\033[0;32m'
NC 			='\033[0m' # No Color
#state values
NOT_DONE 	="${GREEN}\xE2\x9C\x93${NC}"	#nok checkmark
DONE 		="${RED}\xE2\x9C\x97${NC}"		#ok checkmark
DONE_ERROR 	="\xE2\x98\xA0"					#skull

#state
state = {
'get_users':	NOT_DONE,
'get_groups':	NOT_DONE,
'get_acls':		NOT_DONE,
'get_full':		NOT_DONE,
'put_users':	NOT_DONE,
'put_groups':	NOT_DONE,
'put_acls':		NOT_DONE,
'put_full':		NOT_DONE
}
