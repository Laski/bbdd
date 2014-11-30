# -*- coding: utf-8 -*-

from interfazbd import InterfazBD
import numpy as np
import pylab
import random


class Estimador(object):
    """Clase base de los estimadores."""

    def __init__(self, db, tabla, columna, parametro=10):
        self.db = db
        self.tabla = tabla
        self.columna = columna
        self.parametro = parametro

        # Construye las estructuras que necesita el estimador.
        self.build_struct()

    def build_struct(self):
        raise NotImplementedError()

    def estimate_equal(self, value):
        raise NotImplementedError()

    def estimate_greater(self, value):
        raise NotImplementedError()

class ClassicHistogram(Estimador):	#Estimador de Piatetsky-Shapiro basado en histogramas clásicos
	def build_struct(self):
		self.db = InterfazBD(self.db)
		consulta_minmax = "SELECT %s(" + self.columna + ") FROM (SELECT " + self.columna + " FROM " \
									   + self.tabla + " GROUP BY " + self.columna + ")"
		minimo = list(self.db.realizar_consulta(consulta_minmax % "MIN"))[0][0]
		maximo = list(self.db.realizar_consulta(consulta_minmax % "MAX"))[0][0]

		self.longitud_bucket = (maximo - minimo) / float(self.parametro)

		self.bordes = [i*self.longitud_bucket for i in range(self.parametro+1)]
		
		hist = [0 for i in range(self.parametro+1)]
		tot = 0
		for valor in self.db.consultar(self.tabla, self.columna):
			valor = list(valor)[0]
			bucket = self.ubicar_valor(valor)
			hist[bucket] += 1
			tot += 1
		self.probabilidades = [hist_value / float(tot) for hist_value in hist]
		print(self.probabilidades)

	def estimate_equal(self, valor):
		bucket = self.ubicar_valor(valor)
		return self.probabilidades[bucket]

	def estimate_greater(self, valor):
		bucket = self.ubicar_valor(valor)
		minimo = sum(self.probabilidades[:bucket])
		maximo = minimo + self.probabilidades[bucket]
		return (minimo + maximo)/2

	def ubicar_valor(self, valor):
		return int(valor / self.longitud_bucket)

class DistributionSteps(Estimador):	#Estimador de Piatetsky-Shapiro basado en Distribution Steps
	def build_struct(self):
		pass

	def estimate_equal(self, valor):
		pass

	def estimate_greater(self, valor):
		pass

class EstimadorPropio(Estimador):
	def build_struct(self):
		pass

	def estimate_equal(self, valor):
		pass

	def estimate_greater(self, valor):
		pass

