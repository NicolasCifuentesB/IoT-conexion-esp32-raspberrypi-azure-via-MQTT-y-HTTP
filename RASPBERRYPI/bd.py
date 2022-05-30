import sqlite3

base = input('Nombre de la base de datos: ')
conexion = sqlite3.connect(base)
cursor = conexion.cursor()

print('(id,Registro,Temperatura,Humedad)')
for row in cursor.execute('select * from Sensor;') : print(row)

conexion.close()
