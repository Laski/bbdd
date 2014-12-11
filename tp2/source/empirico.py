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


def graficar(archivo, datos):
    plt.clf()
    x = []
    y = []
    for p in sorted(datos.keys()):
        x.append(p)
        y.append(datos[p])
    plt.errorbar(x, y)
    plt.savefig(archivo)


def calcular_error(archivo, tipo_estimador, tipo):
    # 'tipo' debe ser "equal" o "greater"
    errores = {}   # diccionario 'p' -> error medio
    for p in (20, 40, 60, 80, 100):
        if tipo_estimador == "classic":
            estimador = estimators.ClassicHistogram(archivo, 'datos', 'c', p)
        elif tipo_estimador == "steps":
            estimador = estimators.DistributionSteps(archivo, 'datos', 'c', p)
        perfecto  = estimators.EstimadorPerfecto(archivo, 'datos', 'c', p)
        bd = InterfazBD(archivo)
        if tipo == "equal":
            errores[p] = calcular_performance_global(estimador.estimate_equal,   perfecto.estimate_equal)
        elif tipo == "greater":
            errores[p] = calcular_performance_global(estimador.estimate_greater, perfecto.estimate_greater)
    return errores


def process():
    tipo_estimadores = ("classic", "steps")
    seleccionadores = ("equal", "greater")
    distribuciones = ("normal", "uniforme")
    for distribucion in distribuciones:
        archivo = "datasets/" + distribucion + ".sqlite3"
        for seleccionador in seleccionadores:
            for tipo_estimador in tipo_estimadores:
                performance = calcular_error(archivo, tipo_estimador, seleccionador)
                grafico = "datasets/img/" + distribucion + tipo_estimador.title() + seleccionador.title() + ".png"
                graficar(grafico, performance)


if __name__ == "__main__":
    process()
