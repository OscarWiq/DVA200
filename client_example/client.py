#!/usr/bin/env python
# Authors: Oscar & Gustav 

import threading
import json
import requests
from requests.auth import HTTPBasicAuth
import web
from hashlib import blake2b


# LED CONTROLS
#import RPi.GPIO as GPIO

##pin definitions
#LED1 = 11
#LED2 = 13

##GPIO settings
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(LED1, GPIO.OUT)
#GPIO.setup(LED2, GPIO.OUT)

#def led_control(temp_msg):
#    if temp_msg == "01":
#        print ("LED1 on: ", temp_msg)
#        GPIO.output(LED1, GPIO.HIGH)
#    elif temp_msg == "10":
#        print ("LED2 on", temp_msg)
#        GPIO.output(LED2, GPIO.HIGH)
#    elif temp_msg == "11":
#        GPIO.outpout(LED2, GPIO.LOW)
#    else:
#        print ("LED off: ", temp_msg)
#        GPIO.output(LED1, GPIO.LOW)
#        GPIO.output(LED2, GPIO.LOW)

def pw_handler(val):
	h = blake2b(digest_size=20)
	h.update(val.encode('utf-8'))
	digest = h.hexdigest()
	return digest

#params
param_user = "username"
param_pw = "password"
param_id = "id"

#init
learn = False

def reader():

	global learn

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
				try:
					res = web.post(pw)
					if res.status_code == 201:
						user_id = res.json()[param_id]
						print(str(user_id) + ' ' + pw + ' was created via POST.')
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
				try:
					res = web.delete(pw)
					if res.status_code == 200:
						print(str(res.json()[param_id]) + ' ' + ' removed via DELETE /')
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
				try:
					res = web.get(pw)
					if res.status_code == 200:
						print(str(res.json()) + ' ' + pw + ' sent GET /' ) # typ tänd lampa
					else:
						print(f"Something went wrong. Code: {res.status_code}")
				except:
					pass
		else:
			learn = False


def main():

	try:
		threads = []

		t1 = threading.Thread(target=reader)
		t1.start()
		threads.append(t1)
		print(threading.enumerate())
		for thread in threads:
			thread.join()

	except KeyboardInterrupt:
		#GPIO.cleanup()
		print ("Program Exited Cleanly")

if __name__ == "__main__":
	main()
		