# -*- coding: utf-8 -*-

import estimators
import sys
import getopt
from interfazbd import InterfazBD
import os.path


# def main(argv):
#   inputfile = ''
#   outputfile = ''
#   try:
#     opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#   except getopt.GetoptError:
#     print 'empirico.py -i <inputfile>'
#     sys.exit(2)
#   for opt, arg in opts:
#     if opt == '-h':
#       print 'empirico.py -i <inputfile>'
#       sys.exit()
#     elif opt in ("-i", "--ifile"):
#       inputfile = arg
#   process(inputfile)


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

def output(archivo, datos):
  with open(archivo, 'w') as f:
    for item in datos:
      print>>f, item



def calcular_error(archivo, tipo):
  # 'tipo' debe ser "equal" o "greater"
  print tipo.upper()
  erroresClassic = []
  erroresStep = []
  for p in (20, 40, 60, 80, 100):
    classicEstimator = estimators.ClassicHistogram(archivo,  'datos', 'c', p)
    stepEstimator    = estimators.DistributionSteps(archivo, 'datos', 'c', p)
    perfectEstimator = estimators.EstimadorPerfecto(archivo, 'datos', 'c', p)
    bd = InterfazBD(archivo)
    if tipo == "equal":
      errorClassic = calcular_performance_global(classicEstimator.estimate_equal, perfectEstimator.estimate_equal)
      errorStep    = calcular_performance_global(stepEstimator.estimate_equal,    perfectEstimator.estimate_equal)
    elif tipo == "greater":
      errorClassic = calcular_performance_global(classicEstimator.estimate_greater, perfectEstimator.estimate_greater)
      errorStep    = calcular_performance_global(stepEstimator.estimate_greater,    perfectEstimator.estimate_greater)
    erroresClassic.append((p, errorClassic))
    erroresStep.append(   (p, errorStep))
  salidaClassic = archivo + "." + tipo + "Classic.txt"
  salidaStep = archivo + "." + tipo + "Step.txt"
  output(salidaClassic, erroresClassic)
  output(salidaStep, erroresStep)
  

def process(archivo):
  calcular_error(archivo, "equal")
  calcular_error(archivo, "greater")


if __name__ == "__main__":
  #  main(sys.argv[1:])
  process("datasets/normal.sqlite3")
  process("datasets/uniforme.sqlite3")
