
import paho.mqtt.client as mqtt
import sqlite3
import datetime
from azure.iot.device import IoTHubDeviceClient, Message

def iothub_client_init():
	# Create an IoT Hub client
	CONNECTION_STRING = "HostName=axuregateway.azure-devices.net;DeviceId=raspberrypi;SharedAccessKey=S0eftETEH4qSETiEcHlsVokurlESI3NCkBhQgT/drck="
	client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
	return client

def azure_upload(temperature,humedity,light,ground,azure_client) :

	try :
		message_json = '{{"From": "Esp32-Pi","To": "Azure","Temperature": {t},"Humedity" {h},"Brightness": {l},"Ground_H" {g}}}'.format(t = temperature, h = humedity, l = light, g = ground)
		#message_json = '{{"From": "Esp32-Pi","To": "Azure","Temperature": {t},"Humedity" {h}}}'.format(t = temperature, h = humedity)
		message = Message(message_json)
		# Send the message.
		print("Sending message: {}".format(message))
		azure_client.send_message(message)
		print("Message successfully sent")

	except KeyboardInterrupt :
		print("Some stop")


def query(temperatura,humedad,luminosidad,humedad_tierra,cursor,conexion) :
	now = datetime.datetime.now()
	cursor.execute(f'insert into Sensor (Registro,Humedad,Celcius,Luminosidad,Humedad_tierra) values (?,?,?,?,?);',(now,humedad,temperatura,luminosidad,humedad_tierra))
	#cursor.execute(f'insert into Sensor (Registro,Humedad,Celcius,Luminosidad,Humedad_tierra) values (?,?,?,0,0);',(now,humedad,temperatura))
	conexion.commit()

def on_connect(client,userdata,flags,rc) :
	print('Se conecto con mqtt'+str(rc))
	client.subscribe('temp_humidity')

def on_message(client,userdata,msg) :
	if msg.topic == 'temp_humidity' :
		temperature,humedity,light,ground = str((msg.payload.decode())).split(',')
		#temperature,humedity = str((msg.payload.decode())).split(',')
		print(f'Temperatura es: {temperature} °C')
		print(f'Humedad es: {humedity} %')
		print(f'Luminosidad: {light}')
		print(f'Humedad en tierra: {ground} %')
		query(float(temperature),float(humedity),float(light),float(ground),cursor,conexion)
		#query(float(temperature),float(humedity),cursor,conexion)
		azure_upload(temperature,humedity,light,ground,azure_client)
		#azure_upload(temperature,humedity,0,0,azure_client)
	#print(msg.topic + ' ' + str(msg.payload.decode()))


azure_client = iothub_client_init()
conexion = sqlite3.connect('mqtt.db')
cursor = conexion.cursor()

try :
	cursor.execute('''create table Sensor(
	id integer primary key autoincrement,
	Registro timestamp not null,
	Humedad float not null,
	Celcius float not null,
	Luminosidad float not null,
	Humedad_tierra float not null);''')
	print('Se creo la base de datos')
except :
	print('Ya existe la base de datos')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.227.195',1883,60)

client.loop_forever()

conexion.close()
