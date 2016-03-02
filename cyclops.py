#!/usr/bin/env python

import json
import time
import math
import thread

from threading import Thread

from noob import *
import paho.mqtt.client as mqtt

display = LCDDisplay().initialize({
  'name': "bobDisplay",
  'message': "BOB|->Next()"
})

blueLed = Led().initialize({
  'name': "blueLed",
  'digitalPort':2, 
  'pinMode':"OUTPUT"
})

blueLed.switchOn()

# distance
ultrasonicRanger = UltrasonicRanger().initialize({
  'name': "Ranger",
  'digitalPort': 6
})

# meep meep
buzzer = Buzzer().initialize({
  'name': "Buzzer",
  'digitalPort': 5
})


mqttc = mqtt.Client()

display.setText("Hi! This is bob.next() :)").blue()

    
def startPublishingData(mqttClient):
  while True:
    try:
      distance = ultrasonicRanger.distance()

      mqttClient.publish("sensors/distance", json.dumps({
        'distance': distance
      }))

      display.setText("Distance: "+str(distance)).magenta().console()

      time.sleep(2)
    except (IOError,TypeError) as e:
      print e

def on_connect(client, userdata, rc):
  display.setText("Connected with result code "+str(rc)).yellow().console()
  
  #buzzer.buzz(1)

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("orders/")

def yo():
  blueLed.blinkOnce(0.5)

def hi():
  print("...\n")

def on_message(client, userdata, msg):
  infos = json.loads(msg.payload)

  t = Thread(target=yo)
  t.start()

  display.setText(
        msg.topic+":"+ str(infos["cmd"])
    ).cyan().console()

def startMQTTCli():
  mqttc.on_connect = on_connect
  mqttc.on_message = on_message

  #display.setText("Please wait ...").cyan()
  #time.sleep(10) #wait for the broker

  mqttc.connect("zeiracorp.local", 1883, 60)
  
  mqttc.loop_forever()

try:
  thread.start_new_thread( startMQTTCli, () )
  thread.start_new_thread(startPublishingData(mqttc), ())

except Exception as e:
   print e

while 1:
  pass

