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

whiteLed = Led().initialize({
  'name': "whiteLed",
  'digitalPort':2, 
  'pinMode':"OUTPUT"
})

#whiteLed.switchOn()
whiteLed.blinkOnce(0.5)

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


#mqttc = mqtt.Client()
mqttc = mqtt.Client(client_id="SensorsModule", clean_session=True, userdata=None, protocol="MQTTv311")


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
  client.subscribe("motion/meepmeep")

def on_message(client, userdata, msg):
  infos = json.loads(msg.payload)

  display.setText(
        msg.topic+":"+ str(infos["action"])
    ).cyan().console()
  whiteLed.blinkOnce(1)
  buzzer.buzz(1)

def startMQTTCli():
  mqttc.on_connect = on_connect
  mqttc.on_message = on_message

  mqttc.connect("zeiracorp.local", 1883, 60)
  
  mqttc.loop_forever()

try:
  thread.start_new_thread( startMQTTCli, () )
  thread.start_new_thread(startPublishingData(mqttc), ())

except Exception as e:
   print e

while 1:
  pass

