#!/usr/bin/env python
# Authors: Oscar & Gustav 

import json
import requests
from requests.auth import HTTPBasicAuth
import web
from hashlib import blake2b

with open ("tags.json", "r") as f:
	d = json.load(f)
tags = d

def get_key(val):
	for key, value in tags.items():
		if val == value:
			return key
	return 0

def pw_handler(val):
	h = blake2b(digest_size=20)
	h.update(val.encode('utf-8'))
	digest = h.hexdigest()
	return digest

#params
param_usr = "username"
param_pw = "password"

#init
pw = "oscar"

learn = True
#learn = "del"
cnt = 0
while True:

	pw = input()
	if len(pw) is not 0 and pw is not "":

		if pw[0] == "&":
			learn = True
			pw = pw[1:]

		elif pw[0] == "*":
			learn = "del"
			pw = pw[1:]

		else:
			learn = False

		if learn == True:
			pw = pw_handler(pw)
			if pw not in tags.values():
				usr = str(len(tags) + 2)
				res = web.post(usr, pw)
				if res == 201:
					print(usr + ' ' + pw + ' was created via POST.')
					tags[usr] = pw
					with open('tags.json', 'w') as f:
						f.write(json.dumps(tags))
				elif res == 0:
					print("post() error: expected usr, pw")
					exit()
				else:
					print(f"Something went wrong. Code: {res.status_code}")
					exit()

		elif learn == "del":
			pw = pw_handler(pw)
			if pw in tags.values():
				usr = get_key(pw)
				id = int(usr)
				res = web.delete(usr, pw, id)
				if res == 200:
					del tags[usr]
					with open('tags.json', 'w') as f:
						f.write(json.dumps(tags))
					print(usr + ' ' + ' removed via DELETE /')
				elif res == 0:
					print("delete() error: expected usr, pw, id")
					exit()
				else:
					print(f"Something went wrong. Code: {res.status_code}")
					exit()

		else:
			pw = pw_handler(pw)
			if pw in tags.values():
				usr = get_key(pw)
				res = web.get(usr, pw)
				if res == 200:
					print(usr + ' ' + pw + ' sent GET /' ) # typ tänd lampa
				else:
					print(f"Something went wrong. Code: {res.status_code}")
			else:
				print(f"User not in tags.json, User: {pw}")
	else:
		learn = False