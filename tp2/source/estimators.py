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


class ClassicHistogram(Estimador):
    """Estimador de Piatetsky-Shapiro basado en histogramas clásicos."""
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
        probabilidad_minima = sum(self.probabilidades[bucket+1:])    # la probabilidad minima es la de todos los buckets mayores sumados
        probabilidad_maxima = sum(self.probabilidades[bucket:])      # la probabilidad maxima es la de todos los buckets mayores o iguales sumados
        return (probabilidad_minima + probabilidad_maxima)/2         # tomo el promedio como sugiere el paper

    def ubicar_valor(self, valor):
        return int((valor - self.minimo) / self.longitud_bucket)


class DistributionSteps(Estimador):
    """Estimador de Piatetsky-Shapiro basado en Distribution Steps."""
    def build_struct(self):
        consulta_cantidad = "SELECT COUNT(" + self.columna + ") FROM " + self.tabla
        self.cantidad = list(self.db.realizar_consulta(consulta_cantidad))[0][0]

        self.altura_bucket = self.cantidad/self.parametro
        self.separadores = [1+i*self.altura_bucket for i in range(self.parametro)]    # self.separadores tiene las "posiciones" mencionadas en el paper, los puntos de corte
        self.separadores.append(self.cantidad)   # la ultima posicion debe ser siempre la cantidad total de filas, sin importar las cuestiones de redondeo
        print self.separadores
        self.bordes = []    # la idea es que self.bordes[i] = STEP(i). es decir, que tenga los valores limite de cada bucket del histograma
        consulta_ordenada = "SELECT " + self.columna + " FROM " + self.tabla + " ORDER BY " + self.columna + " ASC"
        i = 0
        for valor in self.db.realizar_consulta(consulta_ordenada):
            i += 1  # voy contando la cantidad de registros que veo
            if i in self.separadores:   # estoy en uno de los límites?
                # tengo un nuevo bucket
                valor = valor[0]    # desempaqueto
                self.bordes.append(valor)
        print (self.bordes) #debug
        self.probabilidad_por_bucket = 1.0 / self.parametro

    def estimate_equal(self, valor):
        return 0.5/self.parametro     # no depende del valor

    def estimate_greater(self, valor):
        bucket = self.ubicar_valor(valor)
        buckets_mayores = self.parametro - bucket - 1
        buckets_mayores_o_iguales = self.parametro - bucket
        probabilidad_minima = self.probabilidad_por_bucket * buckets_mayores
        probabilidad_maxima = self.probabilidad_por_bucket * buckets_mayores_o_iguales
        return (probabilidad_minima + probabilidad_maxima)/2

    def ubicar_valor(self, valor):
        limite_inferior = max([limite for limite in self.bordes if limite <= valor])
        return self.bordes.index(limite_inferior)


class EstimadorGrupo(Estimador):
    def build_struct(self):
        pass

    def estimate_equal(self, valor):
        pass

    def estimate_greater(self, valor):
        pass

