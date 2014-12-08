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

	def consultar(self, tablas, columnas, criterios=""):
		consulta = "SELECT " + columnas + " FROM " + tablas + self.armar_where(criterios)
		return self.conexion.execute(consulta)

	def actualizar_registros(self, tabla, cambios, criterios=""):
		# 'cambios' puede ser una lista "columna1=valor1, columna2=valor2..." o "valor1, valor2, ..."
		# 'criterios' es cualquier cosa que acepte un WHERE. podría ser vacío.
		comando = "UPDATE " + tabla + " SET " + cambios + self.armar_where(criterios)
		self.conexion.execute(comando)
		self.commit()

	def borrar_registros(self, tabla, criterio):
		comando = "DELETE FROM " + tabla + " WHERE " + criterio
		self.conexion.execute(comando)
		self.commit()

	def borrar_tabla(self, nombre):
		try:
			self.conexion.execute("DROP TABLE {}".format(nombre))
		except sqlite3.OperationalError as exception:
			if "no such table" in str(exception):
				pass
			else:
				raise

	def mostrar_tablas(self):
		return self.consultar("sqlite_master", "name", "type='table'")

	def armar_where(self, criterio):
		if criterio == "":
			return ""
		else:
			return " WHERE " + criterio

	def crear_indice(self, tabla, nombre, columnas):
		comando = "CREATE INDEX " + nombre + " ON " + tabla + "(" + columnas + ")"
		self.conexion.execute(comando)
		self.commit()

	def listar_tabla(self, tabla):
		comando = "PRAGMA table_info(" + tabla + ")"
		return self.conexion.execute(comando)

	def listar_tablas(self):
		tablas = self.mostrar_tablas()
		res = []
		for tabla in tablas:
			nombre_tabla = tabla[0]
			res.append(nombre_tabla)
			res.append(list(self.listar_tabla(nombre_tabla)))
		return res

	def listar_indices(self, tabla):
		consulta = "PRAGMA index_list(" + tabla + ")"
		return self.conexion.execute(consulta)

	def realizar_consulta(self, consulta):
		# para consultas complejas se puede llamar directamente
		return self.conexion.execute(consulta)


def test():
	bd = InterfazBD("ejemplo.sqlite3")
	bd.borrar_tabla("persona")
	bd.crear_tabla("persona", "nombre text, apellido text, edad integer")
	bd.insertar_registro("persona", ("Nahuel", "Lascano", 23))
	bd.insertar_registro("persona", ("Pablo", "Artuso", 23))
	bd.actualizar_registros("persona", "apellido='Laski'", "nombre='Nahuel'")
	bd.borrar_registros("persona", "apellido='Artuso'")
	bd.crear_indice("persona", "indice1", "apellido")
	print(list(bd.consultar("persona", "*", "")))
	print(list(bd.mostrar_tablas()))
	print(list(bd.listar_tablas()))
	print(list(bd.listar_indices("persona")))




if __name__ == "__main__":
	test()