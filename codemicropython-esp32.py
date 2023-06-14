#http://www.hivemq.com/demos/websocket-client/

#https://wokwi.com/arduino/projects/322577683855704658

import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "smart-city"

sensor = dht.DHT22(Pin(15))
led_pin = Pin(4, Pin.OUT)
pir_pin = Pin(14, Pin.IN, Pin.PULL_UP)
buzzer_pin = Pin(2, Pin.OUT)

def play_buzzer(duration):
    buzzer_pin.on()
    time.sleep(duration)
    buzzer_pin.off()

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

prev_weather = ""
prev_motion = 0
while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure()
    message = ujson.dumps({
        "temp": sensor.temperature(),
        "humidity": sensor.humidity(),
    })
    if message != prev_weather:
        print("Weather updated!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        prev_weather = message
        
        temperature = sensor.temperature()
        if temperature > 25:
            play_buzzer(0.5)  # Toca o buzzer por 500 ms
        else:
            buzzer_pin.off()
        
    else:
        print("No change in weather")
    
    motion = pir_pin.value()
    if motion != prev_motion:
        print("Motion detected: {}".format(motion))
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, motion))
        client.publish(MQTT_TOPIC, str(motion))
        prev_motion = motion
    
    time.sleep(1)
