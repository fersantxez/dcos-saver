#!/usr/bin/env python
#
# post_users.py: load from file and restore users to a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Post a set of users to a running DC/OS cluster, read from a file 
# where they're stored in raw JSON format as received from the accompanying
# "get_users" script.

#reference:
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/users/put_users_uid

import sys
import os
import requests
import json
import env        #environment variables and constants
import helpers      #helper functions in separate module helpers.py

def post_users ( DCOS_IP ):
  """ 
  Get the list of Users from the buffer and post it to a DC/OS cluster 
  available at the DCOS_IP argument.
  """ 
  
  config = helpers.get_config( env.CONFIG_FILE )  
  try:  
    users_file = open( env.USERS_FILE, 'r' )  
  except IOError as error:
    helpers.log(
      log_level='ERROR',
      operation='LOAD',
      objects=['Users'],
      indx=0,
      content=error
      )
    return False #return Error if file isn't available

  #load entire text file and convert to JSON - dictionary
  users = json.loads( users_file.read() )
  users_file.close()

  #loop through the list of users and
  #PUT /users/{uid}
  for index, user in ( enumerate( users['array'] ) ): 

    uid = user['uid']
    #build the request
    api_endpoint = '/acs/api/v1/users/'+uid
    url = 'http://'+config['DCOS_IP']+api_endpoint
    headers = {
    'Content-type': 'application/json',
    'Authorization': 'token='+config['TOKEN'],
    }
    data = {
    'description': user['description'],
    'password': config['DEFAULT_USER_PASSWORD']
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
        objects=['Users'],
        indx=0,
        content=request.status_code
        )
    except requests.exceptions.HTTPError as error:
      helpers.log(
        log_level='ERROR',
        operation='PUT',
        objects=['Users'],
        indx=0,
        content=request.status_code
        )
      return False

    helpers.log(
      log_level='INFO',
      operation='PUT',
      objects=['Users'],
      indx=0,
      content='* DONE *'
      )

    get_input( message=env.MSG_PRESS_ENTER )

    return True

def post_users_groups ( DCOS_IP ):
  """ 
  Get the list of Users_Groups associated with Users from the buffer and post it 
  to a DC/OS cluster available at the DCOS_IP argument.
  """

  config = helpers.get_config( env.CONFIG_FILE )
  try:    
    #open the GROUPS file and load the LIST of groups from JSON
    users_groups_file = open( env.USERS_GROUPS_FILE, 'r' )
    helpers.log(
      log_level='INFO',
      operation='LOAD',
      objects=['Users', 'Groups'],
      indx=0,
      content='** OK **'
      )
  except IOError as error:
    helpers.log(
      log_level='ERROR',
      operation='LOAD',
      objects=['Users', 'Groups'],
      indx=0,
      content=error
      )
    return False

  #load entire text file and convert to JSON - dictionary
  users_groups = json.loads( users_groups_file.read() )
  users_groups_file.close()

  for index, user_group in ( enumerate( users_groups['array'] ) ): 
    #PUT /users/{uid}/users/{uid}
    uid = helpers.escape( user_group['uid'] ) 

    #array of groups for this users_groups
    for index2, group in ( enumerate( user_group['groups'] ) ): 

      gid = group['group']['gid']
      #build the request
      api_endpoint = '/acs/api/v1/users/'+uid+'/groups/'+gid
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
          objects=[ 'Users: '+uid,'Groups: '+gid ],
          indx=index2,
          content=request.status_code
          ) 
      except requests.exceptions.HTTPError as error:
        helpers.log(
          log_level='ERROR',
          operation='PUT',
          objects=[ 'Users: '+uid , 'Groups: '+gid],
          indx=index2,
          content=error
          ) 

  helpers.log(
    log_level='INFO',
    operation='PUT',
    objects=['Users', 'Groups'],
    indx=0,
    content='* DONE *'
    )

  get_input( message=env.MSG_PRESS_ENTER )

  return True
