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
import helpers      #helper functions in separate module helpers.py

def post_users ( DCOS_IP, load_path ):
  """ Get the list of Users from the load_path provided as an argument,
  and post it to a DC/OS cluster available at the DCOS_IP argument.
  """ 

  try:  
    #open the users file and load the LIST of Users from JSON
    users_file = open( load_path, 'r' )
    log(
      log_level='INFO',
      operation='LOAD',
      objects=['Users'],
      indx=0,
      content='** OK **'
      )    
  except IOError as error:
    log(
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
      log(
        log_level='INFO',
        operation='PUT',
        objects=['Users'],
        indx=0,
        content=request.status_code
        )
    except requests.exceptions.HTTPError as error:
      log(
        log_level='ERROR',
        operation='PUT',
        objects=['Users'],
        indx=0,
        content=request.status_code
        )

    log(
      log_level='INFO',
      operation='PUT',
      objects=['Users'],
      indx=0,
      content='* DONE *'
      )

    return True
