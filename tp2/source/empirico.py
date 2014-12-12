# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import estimators
from interfazbd import InterfazBD


def calcular_performances_intermedias(metodo_testeable, metodo_perfecto, valores_consultas):
    res = []
    for i in valores_consultas:
        real = metodo_perfecto(i)
        estimado = metodo_testeable(i)
        res.append(abs(real - estimado))
    return res


def calcular_performance_global(metodo_testeable, metodo_perfecto):
    valores_consultas = range(1, 1000, 10)
    performances_intermedias = calcular_performances_intermedias(metodo_testeable, metodo_perfecto, valores_consultas)
    return sum(performances_intermedias) / len(valores_consultas)


def calcular_error(archivo, tipo_estimador, tipo):
    # 'tipo' debe ser "equal" o "greater"
    errores = {}   # diccionario 'p' -> error medio
    for p in range(10, 200, 10):
        if tipo_estimador == "classic":
            estimador = estimators.ClassicHistogram(archivo, 'datos', 'c', p)
        elif tipo_estimador == "steps":
            estimador = estimators.DistributionSteps(archivo, 'datos', 'c', p)
        elif tipo_estimador == "propio":
            estimador = estimators.EstimadorGrupo(archivo, 'datos', 'c', p)
        perfecto  = estimators.EstimadorPerfecto(archivo, 'datos', 'c', p)
        bd = InterfazBD(archivo)
        if tipo == "equal":
            errores[p] = calcular_performance_global(estimador.estimate_equal,   perfecto.estimate_equal)
        elif tipo == "greater":
            errores[p] = calcular_performance_global(estimador.estimate_greater, perfecto.estimate_greater)
    return errores


def graficar(archivo, datos):
    def getxy(datos):
        # transforma un diccionario en dos arreglos key, value
        x = []
        y = []
        for p in sorted(datos.keys()):
            x.append(p)
            y.append(datos[p])
        return x, y
    plt.clf()
    for tipo_estimador in datos:
        x, y = getxy(datos[tipo_estimador])
        plt.errorbar(x, y, label=tipo_estimador.title())
    plt.xlabel("Parametro S")
    plt.ylabel("Error medio")
    plt.legend()
    plt.savefig(archivo)


def process():
    distribuciones = ("normal", "uniforme")
    seleccionadores = ("equal", "greater")
    tipos_estimadores = ("classic", "steps", "propio")
    for distribucion in distribuciones:
        archivo = "datasets/" + distribucion + ".sqlite3"
        for seleccionador in seleccionadores:
            performance = {}
            for tipo_estimador in tipos_estimadores:
                performance[tipo_estimador] = calcular_error(archivo, tipo_estimador, seleccionador)
            grafico = "datasets/img/" + distribucion + seleccionador.title() + ".png"
            graficar(grafico, performance)
            plt.clf()


if __name__ == "__main__":
    process()
