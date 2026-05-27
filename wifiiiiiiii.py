from machine import Pin , PWM , ADC , I2C
import network
import time
from umqtt.robust import MQTTClient
from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
print("Wifi Connect Success")

mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  port=1883)
mqtt.connect()
print("MQTT connected")

iot_led = Pin(12, Pin.OUT)
iot_led.value(1)

ldr = ADC(Pin(36))

while True:
    value = ldr.read()
    mqtt.publish("gdd/mayo/light", str(value))
    iot_led.value(0)
    time.sleep(1)
    iot_led.value(1)
    time.sleep(1)