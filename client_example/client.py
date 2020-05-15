#!/usr/bin/env python
# Authors: Oscar & Gustav 

import threading
import json
import requests
from requests.auth import HTTPBasicAuth
import web
from hashlib import blake2b
from gpiozero import Button
from time import sleep
import RPi.GPIO as GPIO

#pin definitions
LED1 = 11
LED2 = 13
LED3 = 17
BUTTON = 18

#GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

def led_control(temp_msg):
    if temp_msg == "01":
        print ("LED1 on: ", temp_msg)
        GPIO.output(LED1, GPIO.HIGH)
    elif temp_msg == "10":
        print ("LED2 on", temp_msg)
        GPIO.output(LED2, GPIO.HIGH)
    elif temp_msg == "11":
        GPIO.outpout(LED2, GPIO.LOW)
    else:
        print ("LED off: ", temp_msg)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)

def blink(LED):
	GPIO.output(LED, GPIO.HIGH)
	sleep(1)
	GPIO.output(LED, GPIO.LOW)
	sleep(1)

def led_blinker(temp_msg):
	if temp_msg == "01":
		for n in range(0,4):
			blink(LED1)
	elif temp_msg == "10":
		for n in range(0,4):
			blink(LED2)
	elif temp_msg == '11':
		for n in range(0,4):
			blink(LED3)

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
learn = 0

def button_control():
	global learn
	button = Button(BUTTON)

	while True:
		button.wait_for_press()
		print("The button was pressed!")
		learn = learn + 1
		print(learn, "presses so far")
		if button.wait_for_press() and learn == 1:
			led_control('00')
			led_control('01')

		elif button.wait_for_press() and learn == 2:
			led_control('00')
			led_control('01')

		else:
			led_control('00')
			learn = 0

		sleep(0.5)
		button.wait_for_release()


def reader():

	global learn

	#with open('/dev/tty0', 'r') as tty:
		# below block needs to be indented to account for this open file
	while True:

		# read from rfid
		#pw = tty.readline()

		# simulate reading
		pw = input()

		if len(pw) != 0 and pw != "":

			# simulate button state
			if pw[0] == "&": # LEARN
				learn = 1
				pw = pw[1:]

			elif pw[0] == "*": # DELETE
				learn = 2
				pw = pw[1:]

			else:
				learn = 0 # AUTH

			if learn == 1:

				pw = pw_handler(pw)
				try:
					res = web.post(pw)
					if res.status_code == 201:
						print(str(res.json()[param_id]) + ' ' + pw + ' was created via POST.')
						led_blinker('01')
					elif res == 0:
						print("post() error: expected user_id, pw")
						exit()
					else:
						print(f"Something went wrong. Code: {res.status_code}")
						exit()
				except:
					pass

			elif learn == 2:

				pw = pw_handler(pw)
				try:
					res = web.delete(pw)
					if res.status_code == 200:
						print(str(res.json()[param_id]) + ' ' + ' removed via DELETE /')
						led_blinker('10')
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
						led_blinker('11')
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
		t2 = threading.Thread(target=button_control)
		threads.append(t1)
		threads.append(t2)
		for thread in threads:
			thread.start()
		print(threading.enumerate())
		for thread in threads:
			thread.join()

	except KeyboardInterrupt:
		#GPIO.cleanup()
		print ("Program Exited Cleanly")

if __name__ == "__main__":
	main()
		
