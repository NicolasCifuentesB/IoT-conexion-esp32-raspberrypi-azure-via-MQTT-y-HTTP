import network
import urequests
from machine import Pin
from time import sleep
import dht 

url = 'http://192.168.227.195:5000'
sensor = dht.DHT11(Pin(15))

station = network.WLAN(network.STA_IF)
station.active(True)

if not station.isconnected() :
    station.connect('Nicolas1','clavejeje')
    print(station.ifconfig())
else :
    print(station.ifconfig())

while True:
  try:
    sensor.measure()
    temperature = sensor.temperature()
    humedity = sensor.humidity()
    #msg = (b'{0:3.1f},{1:3.1f},{2:3.1f},{3:3.1f}'.format(temperature,humedity,luz,tierra)) 
    #data = {'Temperature':temperature,'Humedity':humedity,'Luz':luz,'Tierra':tierra}
    data = {'Temperature':temperature,'Humedity':humedity}
    #request = urequests.post(url=url,json=data)
    #print(request.text)
    sleep(2)
  except OSError as e:
    print('Error al leer el sensor.')
    sleep(2)
