#!/usr/bin/env python
#
# post_ldap.py: load from file and restore LDAP configuration to a DC/OS cluster
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Post LDAP configuration to a running DC/OS cluster, read from a file 
# where it's stored in raw JSON format as received from the accompanying
# "get_ldap" script.

#reference:
#https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/iam-api/#!/ldap/put_ldap_config

import sys
import os
import requests
import json
import helpers      #helper functions in separate module helpers.py

def post_ldap ( DCOS_IP, load_path ):
  """ 
  Get the LDAP configuration from the load_path provided as an argument,
  and post it to a DC/OS cluster available at the DCOS_IP argument.
  """ 

  try:  
    #open the LDAP file and load the LDAP configuration from JSON
    ldap_file = open( load_path, 'r' )
    log(
      log_level='INFO',
      operation='LOAD',
      objects=['LDAP'],
      indx=0,
      content='** OK **'
      )    
  except IOError as error:
    log(
      log_level='ERROR',
      operation='LOAD',
      objects=['LDAP'],
      indx=0,
      content=error
      )
    return False #return Error if file isn't 

  #load entire text file and convert to JSON - dictionary
  ldap_config = json.loads( ldap_file.read() )
  ldap_file.close()

  #build the request
  api_endpoint = '/acs/api/v1/ldap/config/'
  url = 'http://'+config['DCOS_IP']+api_endpoint
  headers = {
  'Content-type': 'application/json',
  'Authorization': 'token='+config['TOKEN'],
  }
  data = ldap_config
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
      objects=['LDAP'],
      indx=0,
      content=request.status_code
    )
  except requests.exceptions.HTTPError as error:
      log(
        log_level='ERROR',
        operation='PUT',
        objects=['LDAP'],
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
