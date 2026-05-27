from machine import Pin , PWM , ADC , I2C
import network
import time
import json
from umqtt.robust import MQTTClient
from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS

topic = "xxx/xxx"

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
i2c = I2C(1, sda=Pin(4), scl = Pin(5))
i2c.scan()
i2c.writeto(77,bytearray([0]))

while True:
    value = ldr.read()
    data = i2c.readfrom(77,2)
    raw = (data[0] << 8) | data[1]
    if raw & 0x8000:
        raw -= 65536
    temp = raw / 128.0
    senddata = {
        "light" : value,
        "temp" : temp
        }
    mqtt.publish(topic , json.dumps(senddata))
    iot_led.value(0)
    time.sleep(1)
    iot_led.value(1)
    time.sleep(1)
