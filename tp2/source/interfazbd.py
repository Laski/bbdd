# -*- coding: utf-8 -*-

import sqlite3

class InterfazBD:
	def __init__(self, nombre):
		self.conexion = self.conectar(nombre)
		
	def conectar(self, nombre):
		# se conecta a la base ya existente, o si no existe, la crea y se conecta
		return sqlite3.connect(nombre)

	def commit(self):
		self.conexion.commit()

	def crear_tabla(self, nombre, columnas):
		# 'columnas' debe ser un string de la forma "nombre1 tipo1, nombre2 tipo2, ..."
		comando = "CREATE TABLE " + nombre + "(" + columnas + ")"
		self.conexion.execute(comando) 
		self.commit()

	def insertar_registro(self, tabla, registro):
		# 'tabla' es el nombre de la tabla
		# 'registro' debe ser una tupla con un elemento por cada columna de la tabla
		placeholder = "?, "*(len(registro)-1) + "?"
		comando = "INSERT INTO " + tabla + " VALUES (" + placeholder + ")"
		self.conexion.execute(comando, registro)
		self.commit()

	def insertar_registros(self, tabla, registros):
		for registro in registros:
			self.insertar_registro(tabla, registro)
		self.commit()

	def realizar_consulta(self, consulta):
		res = []
		for resultado in self.conexion.execute(consulta):
			res.append(resultado)
		return res

	def borrar_tabla(self, nombre):
		try:
			self.conexion.execute("DROP TABLE {}".format(nombre))
		except sqlite3.OperationalError as exception:
			if "no such table" in str(exception):
				pass
			else:
				raise



def test():
	bd = InterfazBD("ejemplo.sqlite3")
	bd.borrar_tabla("persona")
	bd.crear_tabla("persona", "nombre text, apellido text, edad integer")
	bd.insertar_registro("persona", ("Nahuel", "Lascano", 23))
	bd.insertar_registro("persona", ("Pablo", "Artuso", 23))
	print(bd.realizar_consulta("SELECT * FROM persona"))

if __name__ == "__main__":
	test()