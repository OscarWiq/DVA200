#!/usr/bin/env python
# Authors: Oscar & Gustav 

import json
import requests
from requests.auth import HTTPBasicAuth
import web

param_usr = "username"
param_pw = "password"

pw = "oscar"

learn = False

with open ("tags.json", "r") as f:
	d = json.load(f)
tags = d

def get_key(val):
	for key, value in tags.items():
		if val == value:
			return key
	return 0


while True:

	if learn:
		if pw not in tags.values():
			usr = str(len(tags) + 1)
			res = web.post(usr, pw)
			if res == 201:
				print(usr + " " + pw + " was created via POST.")
				tags[usr] = pw
				with open('tags.json', 'w') as f:
					f.write(json.dumps(tags))
			else:
				print("ERR")
			s = input()
		else:
			print("no banana")
			s = input()
	else:
		if pw in tags.values():
			usr = get_key(pw)
			res = web.get(usr, pw)
			if res == 200:
				print(usr + " " + pw + " sent GET /" ) # typ tänd lampa
			else:
				print("ERR")
			s = input()
		else:
			print("no banana")
			s = input()
