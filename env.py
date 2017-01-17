#!/usr/bin/env python3
#
# env.py: environment variables for other processes in the project to use
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#

import os

CONFIG_FILE=os.getcwd()+'/.config.json'

#Configurable default values
DCOS_IP='127.0.0.1'
DCOS_USERNAME='bootstrapuser'
DCOS_PASSWORD='deleteme'
DEFAULT_USER_PASSWORD='deleteme'
DEFAULT_USER_SECRET='secret'

#directories
WORKING_DIR=os.getcwd()
DATA_DIR=WORKING_DIR+'/data'
SRC_DIR=WORKING_DIR+'/src'
BACKUP_DIR=WORKING_DIR+'/backup'

#data files
USERS_FILE=DATA_DIR+'/users.json'
USERS_GROUPS_FILE=DATA_DIR+'/users_groups.json'
GROUPS_FILE=DATA_DIR+'/groups.json'
GROUPS_USERS_FILE=DATA_DIR+'/groups_users.json'
ACLS_FILE=DATA_DIR+'/acls.json'
ACLS_PERMISSIONS_FILE=DATA_DIR+'/acls_permissions.json'
LDAP_FILE=DATA_DIR+'/ldap.json'
AGENTS_FILE=DATA_DIR+'/agents.json'
SERVICE_GROUPS_FILE=DATA_DIR+'/service_groups.json'

MENU_WIDTH = 80

#Mark for outputs and inputs
MARK = '** > '
MARK_INPUT = '++ > '

#Menu messages
#Login menu
MSG_APP_TITLE 			=	'Mesosphere DC/OS - IAM Config Backup and Restore Utility'
MSG_NO_CONFIG			=	'Program configuration not found. This is normal on a first run. A new configuration will be generated.'
MSG_CURRENT_CONFIG 		=	'Current configuration'
MSG_DCOS_IP 			=	'DC/OS IP or DNS name'
MSG_DCOS_USERNAME 		=	'DC/OS username'
MSG_DCOS_PASSWORD 		=	'DC/OS password'
MSG_DEFAULT_PASSWORD	=	'Default password for restored users'
MSG_TOKEN				=	'Current authentication token'
MSG_IS_OK				=	'Is this configuration ok? (y/n)'
MSG_ENTER_PARAM_CHANGE	=	'Enter parameter to change'
MSG_ENTER_NEW_VALUE		=	MARK_INPUT
MSG_PRESS_ENTER			=	'\nPress ENTER to continue...'
MSG_DONE 				=	'					* DONE *\n'
MSG_ERROR_LOGIN			=	'Error logging into DC/OS. Please check your configuration.'
MSG_ERROR_CONFIG		=	'Error creating configuration.'
MSG_ERROR_NO_GROUPS		=	'Error finding Groups in buffer. Please GET or LOAD Groups into buffer.'
MSG_ERROR_NO_USERS		=	'Error finding Users in buffer. Please GET or LOAD Users into buffer.'
MSG_ERROR_NO_ACLS		=	'Error finding ACLs in buffer. Please GET or LOAD ACLs into buffer.'
MSG_ERROR_NO_LDAP		=	'Error finding LDAP configuration in buffer. Please GET or LOAD LDAP configuration into buffer.'
MSG_ERROR_NO_SERVICE_GROUPS	= 'Error finding Service Groups in buffer. Please GET or LOAD Service Groups into buffer.'

MSG_AVAIL_CONFIGS		=	'Currently available configurations'
MSG_ENTER_CONFIG_LOAD	=	'Enter name of the configuration to load'
MSG_ENTER_CONFIG_SAVE	=	'Please note that saving under the same name as an existing config will OVERWRITE IT!.\nEnter name of the configuration to save '
MSG_CURRENT_USERS		=	'Users currently in buffer: '
MSG_CURRENT_GROUPS		=	'Groups currently in buffer: '
MSG_CURRENT_ACLS		=	'ACLs and permissions currently in buffer: '
MSG_CURRENT_LDAP		=	'LDAP configuration currently in buffer: '
MSG_CURRENT_SERVICE_GROUPS = 'Service Groups currently in buffer: '
#Main menu
MSG_AVAIL_CMD			= 'Available commands: 	'
MSG_ENTER_CMD			= 'Enter commmand: 								'
MSG_LOAD_SAVE			= 'LOAD/SAVE configuration from/to local buffer.'
MSG_LIST_CONFIG			= 'LIST configurations available on disk.		'
MSG_LOAD_CONFIG			= 'LOAD a configuration available on disk.		'
MSG_SAVE_CONFIG			= 'SAVE current local buffer as configuration to disk.'
MSG_SHOW_CONFIG			= 'SHOW Configuration for this application.		'
MSG_GET_MENU			= 'Commands to GET information from DC/OS 		'
MSG_GET_USERS			= 'GET Users from DC/OS cluster.				'
MSG_GET_GROUPS			= 'GET Groups from DC/OS cluster.				'
MSG_GET_ACLS			= 'GET ACLs from DC/OS cluster.					'
MSG_GET_LDAP			= 'GET LDAP configuration from DC/OS cluster.	'
MSG_GET_AGENTS			= 'GET AGENT status from DC/OS cluster			'
MSG_GET_SERVICE_GROUPS	= 'GET Service Groups from DC/OS cluster		'
MSG_GET_ALL				= 'GET ALL config from DC/OS cluster.			'
MSG_PUT_MENU			= 'Commands to RESTORE information to DC/OS 	'
MSG_PUT_USERS			= 'RESTORE Users to DC/OS cluster.				'
MSG_PUT_GROUPS			= 'RESTORE Groups to DC/OS cluster.				'
MSG_PUT_ACLS			= 'RESTORE ACLs to DC/OS cluster.				'
MSG_PUT_LDAP			= 'RESTORE LDAP configuration to DC/OS cluster. '
MSG_PUT_SERVICE_GROUPS	= 'RESTORE Service Groups to DC/OS cluster. 	'
MSG_PUT_ALL				= 'RESTORE ALL config to DC/OS cluster.			'
MSG_CHECK_MENU			= 'CHECK current local buffer configuration.	'
MSG_CHECK_USERS			= 'CHECK Users in local buffer.					'
MSG_CHECK_GROUPS		= 'CHECK Groups in local buffer.				'
MSG_CHECK_ACLS			= 'CHECK ACLs in local buffer.					'
MSG_CHECK_LDAP			= 'CHECK LDAP configuration in local buffer.	'
MSG_CHECK_SERVICE_GROUPS = 'CHECK Service Groups in local buffer.	'
MSG_EXIT				= 'EXIT this application.						'
#Error messages
ERROR_CONFIG_NOT_FOUND 	= 'Configuration not found.						'
ERROR_EMPTY_BUFFER 		= 'Local buffer is empty. Please LOAD or GET before POSTing.'
ERROR_BUFFER_NOT_FOUND	= 'Local buffer not found.						'
ERROR_UNKNOWN_LOG_LEVEL = 'Unknown log level.							'
ERROR_INVALID_OPTION 	= 'Invalid input. Please choose a valid option.	'

#hotkeys - login menu
hotkeys_login = {
'1' : 'DCOS_IP',
'2'	: 'DCOS_USERNAME',
'3' : 'DCOS_PASSWORD',
'4' : 'DEFAULT_USER_PASSWORD'
}

#hotkeys - main menu
hotkeys_main = {
'd' : 'list_configs',
's'	: 'save_configs',
'l' : 'load_configs',
'0' : 'show_config',
'1' : 'get_users',
'2' : 'get_groups',
'3' : 'get_acls',
'z'	: 'get_ldap',
'a' : 'get_agents',
'b'	: 'get_service_groups',
'g' : 'get_all',
'4' : 'post_users',
'5' : 'post_groups',
'6' : 'post_acls',
'k'	: 'post_ldap',
'e'	: 'post_service_groups',
'p' : 'post_all',
'7' : 'check_users',
'8' : 'check_groups',
'9' : 'check_acls',
'j'	: 'check_ldap',
'v'	: 'check_service_groups',
'x' : 'exit',
'~' : 'noop'
}

#secondary functions associated with the primary ones. E.g. "get_groups" with "get_groups_users"
secondary_functions = {
'get_users'		:'get_users_groups',
'get_groups'	:'get_groups_users',
'get_acls'		:'get_acls_permissions',
'get_agents'	:'display_agents',
'post_users'	:'post_users_groups',
'post_groups'	:'post_groups_users',
'post_acls'		:'post_acls_permissions',
'noop'			:'noop'	
}

# y/n input options
yYnN = ['y','Y','n','N']

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
'get_ldap':		NOT_DONE,
'get_agents':	NOT_DONE,
'get_service_groups': NOT_DONE,
'get_full':		NOT_DONE,
'put_users':	NOT_DONE,
'put_groups':	NOT_DONE,
'put_acls':		NOT_DONE,
'put_ldap':		NOT_DONE,
'put_service_groups': NOT_DONE,
'put_full':		NOT_DONE
}
