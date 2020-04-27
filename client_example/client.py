#!/user_id/bin/env python
# Authors: Oscar & Gustav 

import json
import requests
from requests.auth import HTTPBasicAuth
import web
from hashlib import blake2b

with open ("tags.json", "r") as f:
	d = json.load(f)
tags = d

def get_key(val, list):
	for i in list:
		if val == i[param_pw]:
			return i[param_user]
	return 0

def pw_handler(val):
	h = blake2b(digest_size=20)
	h.update(val.encode('utf-8'))
	digest = h.hexdigest()
	return digest

def pw_checker(val, list):
	for i in list:
		if val == i[param_pw]:
			return True
	return False

#params
param_user = "username"
param_pw = "password"
param_id = "id"

#init
pw = "oscar"
learn = False

while True:

	pw = input()
	if len(pw) != 0 and pw != "":

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

			if not pw_checker(pw, tags):
				try:
					res = web.post(pw)
					if res.status_code == 201:
						user_id = res.json()[param_id]
						print(str(user_id) + ' ' + pw + ' was created via POST.')
						
						user = {}
						user[param_user] = user_id
						user[param_pw] = pw
						tags.append(user)
						
						with open('tags.json', 'w') as f:
							f.write(json.dumps(tags))
					elif res == 0:
						print("post() error: expected user_id, pw")
						exit()
					else:
						print(f"Something went wrong. Code: {res.status_code}")
						exit()
				except:
					pass

		elif learn == "del":
			pw = pw_handler(pw)
			if pw_checker(pw, tags):
				try:
					user_id = get_key(pw, tags)
					res = web.delete(str(user_id))
					if res.status_code == 200:

						tags.remove(tags[user_id - 2])
						for i in range(user_id - 2, len(tags)):
							if not tags[i][param_user] == i + 2:
								tags[i][param_user] = i + 2
						
						with open('tags.json', 'w') as f:
							f.write(json.dumps(tags))
						
						print(str(user_id) + ' ' + ' removed via DELETE /')
					elif res == 0:
						print("delete() error: expected user_id")
						exit()
					else:
						print(f"Something went wrong. Code: {res.status_code}")
						exit()
				except:
					pass

		else:
			pw = pw_handler(pw)
			if pw_checker(pw, tags):
				try:
					#user_id = get_key(pw, tags)
					res = web.get(pw)
					if res.status_code == 200:
						print(str(res.json()) + ' ' + pw + ' sent GET /' ) # typ tänd lampa
					else:
						print(f"Something went wrong. Code: {res.status_code}")
				except:
					pass
			else:
				print(f"User not in tags.json")
	else:
		learn = False
		