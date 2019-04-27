#!/usr/bin/env python3
import os
import sys
import uuid
import time
import subprocess
from threading import Thread
import paho.mqtt.client as mqtt

reload(sys)
sys.setdefaultencoding('utf8')


SERVER='srcv.ddns.net'
PORT=9999
TOPIC='teste'

def lerArquivo():
	diretorio = '/var/tmp/bot/'
	while True:
		files = os.listdir(diretorio)
		files.sort()	
		for f in files:
			files = os.listdir(diretorio)
			files.sort()
			os.system("ffplay -nodisp -autoexit '%s' >/dev/null 2>&1" % (diretorio + f))
			os.system("rm " + diretorio + f)

def gtts(texto, arquivo):
	os.system("gtts-cli '%s' --lang pt --output '%s'" % (texto, arquivo))

def on_message(client, userdata, message):
	texto = str(message.payload.decode("utf-8"))
	arquivo = '/var/tmp/bot/' + str(time.time()) + '.mp3'
	Thread(target=gtts, args=[texto, arquivo]).start()

def mqtt_cliente(server, port, topic):
	os.system("mkdir /var/tmp/bot/ ")
	client = mqtt.Client(client_id="BOOT", clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport="tcp")
	client.on_message=on_message
	client.connect(server, port)
	client.subscribe(topic)
	while True:
		client.loop()


Thread(target=lerArquivo, args=[]).start()
Thread(target=mqtt_cliente, args=[SERVER, PORT, TOPIC]).start()







