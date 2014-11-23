# -*- coding: utf-8 -*-

import sqlite3
import numpy as np
import pylab
import random

class Estimador(object):
    """Clase base de los estimadores."""

    def __init__(self, db, table, column, parameter=10):
        self.db = db
        self.table = table
        self.column = column
        self.parameter = parameter

        # Construye las estructuras necesita el estimador.
        self.build_struct()

    def build_struct(self):
        raise NotImplementedError()

    def estimate_equal(self, value):
        raise NotImplementedError()

    def estimate_greater(self, value):
        raise NotImplementedError()

class ClassicHistogram(Estimador):	#Estimador de Piatetsky-Shapiro basado en histogramas clásicos
	def build_struct(self):
		pass

	def estimate_equal(self):
		pass

	def estimate_greater(self):
		pass

class DistributionSteps(Estimador):	#Estimador de Piatetsky-Shapiro basado en Distribution Steps
	def build_struct(self):
		pass

	def estimate_equal(self):
		pass

	def estimate_greater(self):
		pass

class EstimadorPropio(Estimador):
	def build_struct(self):
		pass

	def estimate_equal(self):
		pass

	def estimate_greater(self):
		pass

