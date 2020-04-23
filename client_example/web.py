#!/usr/bin/env python
# Authors: Oscar owt18001 & Gustav gwd17001

import json
import requests
from requests.auth import HTTPBasicAuth

username = "johnchambers"
password = "ciscodisco123"
param_usr = "username"
param_pw = "password"


base_url = "http://127.0.0.1:5000"

def get(usr, pw):
	global username, password
	url = base_url + "/api/login"
	res = requests.get(url, auth=HTTPBasicAuth(usr, pw))
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
	else:
		res = requests.post(url=url, json=body, auth=HTTPBasicAuth(username, password))
		return res.status_code