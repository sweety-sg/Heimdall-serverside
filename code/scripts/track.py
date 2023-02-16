import os
import io
import subprocess
import yaml
import json
import requests
import hmac
import hashlib


with io.open('../configuration/config.yml', 'r') as stream:
	try:
		CONFIG_VARS = yaml.safe_load(stream)
	except yaml.YAMLError as err:
		print(err)
		raise


AUTH_LOG = CONFIG_VARS['AUTH_LOG']
MASTER_URL = CONFIG_VARS['MASTER']['URL']
ENDPOINT_LOG = CONFIG_VARS['MASTER']['ENDPOINT_LOG']
MASTER_SECRET = CONFIG_VARS['MASTER']['SECRET']
AUTHORIZED_KEYS = CONFIG_VARS['DESTINATION_FILE']


def login(log):
	l = log.split()
	print("LOGIN")

	RSAKey = l[-1]
	encodedKeys = subprocess.run(['ssh-keygen', '-lf', AUTHORIZED_KEYS], capture_output=True, text=True).stdout.splitlines()
	
	client = None
	activity = "LOGIN"

	if l[-2] == "RSA":
		activity = "LOGIN_SSH_KEY"
		for x in encodedKeys:
			x = x.split()
			if x[1] == RSAKey:
				client = x[2]
				break
	else:
		activity = "LOGIN_SSH_PWD"

	payload = {
		"month": l[0],
		"date": l[1],
		"time": l[2],
		"host": l[3],
		"user": l[8],
		"ip": l[10],
		"port": l[12],
		"activity": activity,
		"client": client
	}

	send(payload)


def logout(log):
	l = log.split()
	print("LOGOUT")

	payload = {
		"month": l[0],
		"date": l[1],
		"time": l[2],
		"host": l[3],
		"user": l[8],
		"ip": l[9],
		"port": l[11],
		"activity": "LOGOUT_SSH"
	}

	send(payload)


def chusr_open(log):
	l = log.split()
	print("CHUSR_OPEN")

	payload = {
		"month": l[0],
		"date": l[1],
		"time": l[2],
		"host": l[3],
		"user": l[-3],
		"activity": "CHUSR_OPEN",
		"client": l[-1]
	}

	send(payload)


def chusr_close(log):
	l = log.split()
	print("CHUSR_CLOSE")

	payload = {
		"month": l[0],
		"date": l[1],
		"time": l[2],
		"host": l[3],
		"user": l[-1],
		"activity": "CHUSR_CLOSE"
	}

	send(payload)


def send(payload):
	signature  = 'sha1=' + hmac.new(MASTER_SECRET.encode(), json.dumps(payload).encode(), hashlib.sha1).hexdigest()

	headers = {
		'content-type': 'application/json',
		'X-Bipolar-Signature': signature,
	}
	url = MASTER_URL + ENDPOINT_LOG

	f = requests.post(url, json=payload, headers=headers)


def track():

	f = subprocess.Popen(['tail', '-F', AUTH_LOG], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	
	while True:
		line = f.stdout.readline().decode()
		if "sshd" in line:
			if "Accepted" in line:
				login(line)
			elif "Disconnected from user" in line:
				logout(line)
		elif "pam_unix(su:session)" in line:
			if "opened" in line:
				chusr_open(line)
			elif "closed" in line:
				chusr_close(line)

track()
