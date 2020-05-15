#!/usr/bin/env python
# Authors: Oscar owt18001 & Gustav gwd17001

import json
import requests
from requests.auth import HTTPBasicAuth

# read these from secret later
username = "johnchambers"
password = "ciscodisco123"

#params
param_id = "id"
param_usr = "username"
param_pw = "password"

base_url = "https://52.200.1.200:5005"
#base_url = "https://127.0.0.1:5000"

def get(pw):
	url = base_url + "/api/login"
	res = requests.get(url, auth=HTTPBasicAuth(pw, pw), verify=False)
	return res

def post(pw):
	global username, password
	url = base_url + "/api/users"
	body = {
		param_usr : pw,
		param_pw : pw
	}
	if len(pw) == 0 or pw == "":
		return 0
	print(body)
	res = requests.post(url=url, json=body, auth=HTTPBasicAuth(username, password), verify=False)
	return res

def delete(pw):
	global username, password
	if not len:
		return 0
	url = base_url + "/api/users/del/"
	try:
		usr_id = get(pw)
		if usr_id.status_code == 200:
			res = requests.delete(url=url + str(usr_id.json()[param_id]), auth=HTTPBasicAuth(username, password), verify=False)
			return res
		else:
			return usr_id
	except:
		return 0 
	return 0
