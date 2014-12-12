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
            assert tipos_columnas(tablas[i+1])[index_columna] in ('int', 'integer'), "La columna no es de tipo entero"
            return
    assert False, "La tabla no existe o no tiene la columna especificada"


class Estimador(object):
    """Clase base de los estimadores."""
    def __init__(self, db, tabla, columna, parametro=10):
        validar(db, tabla, columna)
        self.nombre_db = db
        self.db = InterfazBD(db)
        self.tabla = tabla
        self.columna = columna
        self.parametro = parametro

        # consultas útiles
        self.consulta_desordenada = "SELECT " + self.columna + " FROM " + self.tabla
        self.consulta_ordenada = "SELECT " + self.columna + " FROM " + self.tabla + " ORDER BY " + self.columna + " ASC"
        self.consulta_min_max = "SELECT %s(" + self.columna + ") FROM (SELECT " + self.columna + " FROM " \
                                + self.tabla + " GROUP BY " + self.columna + ")"
        self.consulta_cantidad_tuplas = "SELECT COUNT(" + self.columna + ") FROM " + self.tabla
        self.consulta_cuenta_ocurrencias = "SELECT " + self.columna + ", COUNT(*) FROM " + self.tabla + " GROUP BY " + self.columna
        self.consulta_cuenta_ocurrencias_personalizada = "SELECT COUNT(" + self.columna + ") FROM " + self.tabla + " WHERE " + self.columna + "%s"
        # valores utiles
        self.n_registros = list(self.db.realizar_consulta(self.consulta_cantidad_tuplas))[0][0]

        # inicializo las estructuras
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
        self.minimo = list(self.db.realizar_consulta(self.consulta_min_max % "MIN"))[0][0]    # hago la consulta por el minimo y la desempaqueto
        self.maximo = list(self.db.realizar_consulta(self.consulta_min_max % "MAX"))[0][0]    # idem para maximo

        self.longitud_bucket = (self.maximo - self.minimo) / float(self.parametro)

        hist = [0 for i in range(self.parametro+1)]     # inicializo el histograma
        for valor in self.db.consultar(self.tabla, self.columna):
            valor = list(valor)[0]  # desmpaqueto
            bucket = self.ubicar(valor)
            hist[bucket] += 1
        self.probabilidades = [hist_value/float(self.n_registros) for hist_value in hist]  # normalizamos el histograma
        # self.probabilidades tiene, para cada bucket, la probabilidad de que un valor de la distribución caiga en ese rango

    def estimate_equal(self, valor):
        # simplemente devuelvo el valor del bucket en el histograma normalizado
        try:
            bucket = self.ubicar(valor)
        except IndexError:
            return 0    # si el valor está fuera del rango, la probabilidad de que uno sea igual a el es 0
        return self.probabilidades[bucket]/self.longitud_bucket

    def estimate_greater(self, valor):
        try:
            bucket = self.ubicar(valor)
        except IndexError:
            return int(valor < self.minimo) # hacky pero anda: si el valor es menor que el minimo la probabilidad es 1,
                                            # sino es mayor que el máximo y entonces es 0
        probabilidad_minima = sum(self.probabilidades[bucket+1:])    # la probabilidad mínima es la de todos los buckets mayores sumados
        probabilidad_maxima = sum(self.probabilidades[bucket:])      # la probabilidad máxima es la de todos los buckets mayores o iguales sumados
        return (probabilidad_minima + probabilidad_maxima)/2         # tomo el promedio entre ambas, como sugiere el paper

    def ubicar(self, valor):
        if valor < self.minimo or valor > self.maximo:
            raise IndexError    # el valor está fuera del rango
        return int((valor-self.minimo) / self.longitud_bucket)       # raro pero creanme que anda


class DistributionSteps(Estimador):
    """
        Estimador de Piatetsky-Shapiro basado en Distribution Steps.
        Elegimos la versión que minimiza el error en el caso promedio.
    """
    def build_struct(self):
        self.altura_bucket = self.n_registros / self.parametro                        # la altura ideal de todos los buckets
        self.separadores = [1+i*self.altura_bucket for i in range(self.parametro)]    # self.separadores tiene las "posiciones" de corte en el arreglo de registros
        self.separadores.append(self.n_registros)   # la ultima posicion debe ser siempre la cantidad total de filas, sin importar las cuestiones de redondeo

        self.bordes = []    # queremos self.bordes[i] = lo que el paper llama STEP(i). es decir, que tenga los valores limite de cada bucket del histograma.
        i = 0
        for (valor, ) in self.db.realizar_consulta(self.consulta_ordenada):
            i += 1  # voy contando la cantidad de registros que veo
            if i in self.separadores:   # estoy en uno de los límites?
                # inauguro un nuevo bucket
                self.bordes.append(valor)
        # computamos delta
        self.delta = min(0.5/self.parametro, self.get_density())   # extraido del paper

    def get_density(self):
        # algoritmo extraido del paper
        acum = sum([ocurrencias**2
                    for valor, ocurrencias in self.db.realizar_consulta(self.consulta_cuenta_ocurrencias)
                    if self.bordes.count(valor < 2)])
        return acum / float((self.n_registros**2))

    def estimate_equal(self, valor):
        # extraido del paper
        if self.entre_bordes(valor) or self.igual_a_uno_no_extremo(valor):
            # caso A y B1
            return self.delta
        if self.igual_a_varios_no_extremos(valor):
            # caso B2
            return self.bordes.count(valor) / self.parametro
        if self.igual_a_varios_incluyendo_extremos(valor):
            # caso C
            if valor == self.bordes[0] == self.bordes[-1]:
                return 1    # todos son iguales
            return (self.bordes.count(valor)-0.5) / self.parametro
        if self.igual_a_un_extremo(valor):
            # caso C1
            return self.delta / 2
        if self.fuera_del_histograma(valor):
            # caso D
            return 0        # ninguno puede ser igual a algo que cae fuera

    def estimate_greater(self, valor):
        # como en el paper están definidas las fórmulas para estimar la probabilidad de que 'valor' sea MENOR (no mayor) que un
        # elemento aleatorio de la distribución, definiremos estimate_lesser() y haremos esta función en base a ella
        return 1 - self.estimate_lesser(valor) - self.estimate_equal(valor)

    def estimate_lesser(self, valor):
        # extraido del paper
        if self.entre_bordes(valor):
            # caso A
            return (self.ubicar(valor)+0.5)/self.parametro - self.delta/2
        if self.igual_a_uno_no_extremo(valor):
            # caso B1
            return self.ubicar(valor)/self.parametro - self.delta/2
        if self.igual_a_varios_no_extremos(valor):
            # caso B2
            return (self.ubicar(valor)-0.5)/self.parametro
        if self.igual_a_varios_incluyendo_extremos(valor):
            # caso C
            if valor == self.bordes[0]:
                return 0    # nadie es menor porque todos son mayores o iguales
            if valor == self.bordes[-1]:
                return 1 - (self.bordes.count(valor)-0.5)/self.parametro
        if self.igual_a_un_extremo(valor):
            # caso C1
            if valor == self.bordes[0]:
                return 0
            if valor == self.bordes[-1]:
                return 1 - self.delta/2
        if self.fuera_del_histograma(valor):
            # caso D
            if valor < self.bordes[0]:
                return 0
            if valor > self.bordes[-1]:
                return 1

    def ubicar(self, valor):
        if valor < self.bordes[0] or valor > self.bordes[-1]:
            raise IndexError    # el valor está fuera del rango
        limite_inferior = max([limite for limite in self.bordes if limite <= valor])
        return float(self.bordes.index(limite_inferior))    # casteo a float porque se lo va a usar para aritmética flotante

    def es_extremo(self, valor):
        return valor == self.bordes[0] or valor == self.bordes[-1]

    def entre_bordes(self, valor):
        # caso A
        return self.bordes.count(valor) == 0 and not self.fuera_del_histograma(valor)

    def igual_a_uno_no_extremo(self, valor):
        # caso B1
        return self.bordes.count(valor) == 1 and not self.es_extremo(valor)

    def igual_a_varios_no_extremos(self, valor):
        # caso B2
        return self.bordes.count(valor) > 1 and not self.es_extremo(valor)

    def igual_a_varios_incluyendo_extremos(self, valor):
        # caso C
        return self.bordes.count(valor) > 1 and self.es_extremo(valor)

    def igual_a_un_extremo(self, valor):
        # caso C1
        return self.bordes.count(valor) == 1 and self.es_extremo(valor)

    def fuera_del_histograma(self, valor):
        # caso D
        return valor < self.bordes[0] or valor > self.bordes[-1]


class EstimadorGrupo(Estimador):
    # usa el parametro para hacer un cache con ese tamaño
    def build_struct(self):
        self.estimador_clasico = ClassicHistogram(self.nombre_db, self.tabla, self.columna, self.parametro) #acá puedo no pasarle parámetro y que sea el default (10) o pasarle el parámetro que me viene, opte por la segunda así el estimador de "respaldo" también mejora a medida que aumenta p
        #self.dict_acum_values = dict(zip(list(sorted(self.dict_cant_values.keys())), list(acum)))
        consulta_cache_igualdad = "SELECT " + self.columna + ", COUNT(*) FROM " + self.tabla + " GROUP BY " + self.columna + " ORDER BY COUNT(*) DESC"
        self.dict_cache_igualdad = dict((x, y) for x, y in [x for x in self.db.realizar_consulta(consulta_cache_igualdad)][:self.parametro])  # cache de tamaño self.parametro
        self.dict_cache_mayor = dict()
        for x in list(self.dict_cache_igualdad):
            consulta = "SELECT COUNT(*) FROM " + self.tabla + " WHERE " + self.columna + " > " + str(x)
            self.dict_cache_mayor[x] = self.db.realizar_consulta(consulta)
        
    def estimate_equal(self, valor):
        if valor in self.dict_cache_igualdad:
            return float(self.dict_cache_igualdad[valor]) / self.n_registros
        else:
            return self.estimador_clasico.estimate_equal(valor)

    def estimate_greater(self, valor):
        if valor in self.dict_cache_mayor:
            return float(self.dict_cache_mayor[valor]) / self.n_registros
        else:
            return self.estimador_clasico.estimate_greater(valor)
    
#    def ubicar_menor_mas_cercano(self, valor):
#        return max([v for v in self.dict_acum_values.keys() if v < valor])


class EstimadorPerfecto(Estimador):
    """ Para comparar. Responde siempre la respuesta correcta, mirando toda la tabla """
    def build_struct(self):
        pass

    def estimate_equal(self, valor):
        consulta = self.consulta_cuenta_ocurrencias_personalizada % ("=" + str(valor))
        ((ocurrencias, ), ) = self.db.realizar_consulta(consulta)
        return float(ocurrencias) / self.n_registros

    def estimate_greater(self, valor):
        consulta = self.consulta_cuenta_ocurrencias_personalizada % (">" + str(valor))
        ((n_mayores, ), ) = self.db.realizar_consulta(consulta)
        return float(n_mayores) / self.n_registros
