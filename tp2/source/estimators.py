# -*- coding: utf-8 -*-

import numpy as np
import pylab
import random

from interfazbd import InterfazBD

def validar(db, tabla, columna):
    def nombres_columnas(columnas):
        return [t[1] for t in columnas]
    def tipos_columnas(columnas):
        return [t[2] for t in columnas]

    db = InterfazBD(db)
    tablas = db.listar_tablas()
    for i in range(0, len(tablas), 2):
        if tablas[i] == tabla and columna in nombres_columnas(tablas[i+1]):
            index_columna = nombres_columnas(tablas[i+1]).index(columna)
            assert 'int' == tipos_columnas(tablas[i+1])[index_columna], "La columna no es de tipo entero"
            return
    assert False, "La tabla no existe o no tiene la columna especificada"
    
class Estimador(object):
    """Clase base de los estimadores."""

    def __init__(self, db, tabla, columna, parametro=10):
        validar(db, tabla, columna)
        self.db = InterfazBD(db)
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

class ClassicHistogram(Estimador):  #Estimador de Piatetsky-Shapiro basado en histogramas clásicos
    def build_struct(self):
        consulta_minmax = "SELECT %s(" + self.columna + ") FROM (SELECT " + self.columna + " FROM " \
                                       + self.tabla + " GROUP BY " + self.columna + ")"
        self.minimo = list(self.db.realizar_consulta(consulta_minmax % "MIN"))[0][0]
        self.maximo = list(self.db.realizar_consulta(consulta_minmax % "MAX"))[0][0]

        self.longitud_bucket = (self.maximo - self.minimo) / float(self.parametro)

        self.bordes = [i*self.longitud_bucket for i in range(self.parametro+1)]     # self.bordes tiene los limites de cada bucket
        
        hist = [0 for i in range(self.parametro+1)]     # inicializo el histograma
        tot = 0     # para ir contando cantidad de registros (se usa para normalizar después)
        for valor in self.db.consultar(self.tabla, self.columna):
            valor = list(valor)[0]
            bucket = self.ubicar_valor(valor)
            hist[bucket] += 1
            tot += 1
        self.probabilidades = [hist_value / float(tot) for hist_value in hist]  # normalizamos el histograma
        # self.probabilidades tiene, para cada bucket, la probabilidad de que un valor de la distribución en ese rango

    def estimate_equal(self, valor):
        bucket = self.ubicar_valor(valor)
        return self.probabilidades[bucket]

    def estimate_greater(self, valor):
        bucket = self.ubicar_valor(valor)
        minima = sum(self.probabilidades[bucket+1:])    # la probabilidad minima es la de todos los buckets mayores
        maxima = sum(self.probabilidades[bucket:])      # la probabilidad maxima es la de todos los buckets mayores o iguales
        return (minima + maxima)/2                      # tomo el promedio como sugiere el paper

    def ubicar_valor(self, valor):
        return int((valor - self.minimo) / self.longitud_bucket)


class DistributionSteps(Estimador): #Estimador de Piatetsky-Shapiro basado en Distribution Steps
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

