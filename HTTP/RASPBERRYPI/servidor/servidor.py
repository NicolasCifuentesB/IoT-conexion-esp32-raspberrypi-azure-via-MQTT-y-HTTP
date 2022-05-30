from flask import Flask
from flask import request
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
		message_json = '{{"From" : "Esp-pi","To" : "Azure", "Temperature" : {t}, "Humedity" : {h}}}'.format(t = temperature, h = humedity)
		message = Message(message_json)
		# Send the message.
		print("Sending message: {}".format(message))
		azure_client.send_message(message)
		print("Message succesfully sent")

	except KeyboardInterrupt :
		print("Some stop")

def query(temperatura,humedad,cursor,conexion) :
	now = datetime.datetime.now()
	cursor.execute(f'insert into Sensor (Registro,Humedad,Celcius,Luminosidad,Humedad_tierra) values (?,?,?,0,0);',(now,humedad,temperatura))
	conexion.commit()

app = Flask(__name__)
azure_client = iothub_client_init()
conexion = sqlite3.connect('http.db',check_same_thread=False)
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

@app.route('/',methods = ['POST','GET'])
def server() :

	if request.method == 'POST' :
		data = request.json
		temperature,humedity = data['Temperature'],data['Humedity']
		print(f'Temperatura: {temperature} °C')
		print(f'Humedad: {humedity} %')
		query(float(temperature),float(humedity),cursor,conexion)
		azure_upload(temperature,humedity,0,0,azure_client)
		return('<p>Temperatura: {}\nHumedad: {}</p>'.format(data['Temperature'],data['Humedity']))
	else :
		return('<p>No post method</p>')
