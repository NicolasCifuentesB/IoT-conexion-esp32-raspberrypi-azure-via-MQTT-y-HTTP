from machine import Pin
from time import sleep
import dht 
from umqtt.simple import MQTTClient

SERVER = '192.168.227.195' # MQTT SERVER ADDRESS (raspberry)
CLIENT_ID = 'ESP32_DHT'
TOPIC = b'temp_humidity'

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()

sensor = dht.DHT11(Pin(15))

while True:
  try:
    sensor.measure()
    temperature = sensor.temperature()
    humedity = sensor.humidity()
    #msg = (b'{0:3.1f},{1:3.1f},{2:3.1f},{3:3.1f}'.format(temperature,humedity,luz,tierra)) 
    msg = (b'{0:3.1f},{1:3.1f}'.format(temperature,humedity))
    client.publish(TOPIC, msg)
    print(msg.decode())
    sleep(2)
  except OSError as e:
    print('Error al leer el sensor.')
    sleep(2)