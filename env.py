#!/usr/bin/env python
#
# env.py: environment variables for other processes in the project to use
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#

CONFIG_FILE="./.config.json"

#Configurable default values
DCOS_IP=127.0.0.1
USERNAME='bootstrapuser'
PASSWORD='deleteme'
DEFAULT_USER_PASSWORD='deleteme'
DEFAULT_USER_SECRET='secret'

#directories
WORKING_DIR='./'
DATA_DIR=WORKING_DIR+'/data'
SRC_DIR=WORKING_DIR+'/src'
BACKUP_DIR=$WORKING_DIR+'/backup'

#data files
USERS_FILE=DATA_DIR+'/users.json'
USERS_GROUPS_FILE=DATA_DIR+'/users_groups.json'
GROUPS_FILE=DATA_DIR+'/groups.json'
GROUPS_USERS_FILE=DATA_DIR+'/groups_users.json'
ACLS_FILE=DATA_DIR+'/acls.json'
ACLS_PERMISSIONS_FILE=DATA_DIR+'/acls_permissions.json'


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
MSG_ENTER_NEW_VALUE		= 'Enter new value: '
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
'1' : 'DCOS_IP',
'2'	: 'DCOS_USERNAME',
'3' : 'DCOS_PW',
'4' : 'DEFAULT_PW'
}

#hotkeys - main menu
hotkeys_main = {
'd' : 'LIST_CONFIG',
'l'	: 'LOAD_CONFIG',
's'	: 'SAVE_CONFIG',
'1' : 'GET_USERS',
'2' : 'GET_GROUPS',
'3' : 'GET_ACLS',
'g' : 'FULL_GET',
'4' : 'PUT_USERS',
'5' : 'PUT_GROUPS',
'6' : 'PUT_ALCS',
'p' : 'FULL_PUT',
'7' : 'CHECK_USERS',
'8' : 'CHECK_GROUPS',
'9' : 'CHECK_ACLS',
'0' : 'CHECK_CONFIG',
'x' : 'EXIT'
}

# y/n input options
yYnN = ['y','Y','n','N']

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
