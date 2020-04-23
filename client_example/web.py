#!/usr/bin/env python
# Authors: Oscar owt18001 & Gustav gwd17001

import json
import requests
from requests.auth import HTTPBasicAuth

# read these from secret later
username = "johnchambers"
password = "ciscodisco123"

#params
param_usr = "username"
param_pw = "password"


base_url = "https://127.0.0.1:5000"

def get(usr, pw):
	url = base_url + "/api/login"
	res = requests.get(url, auth=HTTPBasicAuth(usr, pw), verify=False)
	return res.status_code

def post(usr, pw):
	global username, password
	url = base_url + "/api/users"

	body = {
		param_usr : usr,
		param_pw : pw
	}

	if len(usr) == 0 or len(pw) == 0:
		return 0
	res = requests.post(url=url, json=body, auth=HTTPBasicAuth(username, password), verify=False)
	return res.status_code

def delete(usr, pw, id):
	global username, password
	url = base_url + "/api/users/" + str(id)
	res = requests.get(url, verify=False)
	if int(res.json()['username']) == id:
		del_url = base_url + "/api/users/del/"
		res_del = requests.delete(url=del_url + str(id), auth=HTTPBasicAuth(username, password), verify=False) 
		return res_del.status_code
	return 0
