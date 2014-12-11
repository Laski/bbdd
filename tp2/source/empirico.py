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

def process(archivo):
  #por equal
  print "EQUAL"
  errorClassic = []
  errorStep = []
  for p in (20, 40, 60, 80, 100):
    aEstimator = estimators.ClassicHistogram(archivo, 'datos', 'c1', p)
    bEstimator = estimators.DistributionSteps(archivo, 'datos', 'c1', p)
    bd = InterfazBD(archivo)
    errorA = 0
    errorB = 0
    for i in range(1,101):
      consulta = "select count(c1) from datos where c1=%d" %(i)
      real = bd.realizar_consulta(consulta).fetchone()[0]/float(10000)
      estimadoA = aEstimator.estimate_equal(i)
      estimadoB = bEstimator.estimate_equal(i)
      errorA = errorA + abs(real - estimadoA)
      errorB = errorB + abs(real - estimadoB)
    totalA = errorA / 100
    totalB = errorB / 100
    errorClassic.append((p,totalA))
    errorStep.append((p,totalB))
  salida = archivo + ".equalClassic.txt"
  archivoSalida = open(salida, 'w')
  for item in errorClassic:
    print>>archivoSalida, item
  salida = archivo + ".equalStep.txt"
  archivoSalida = open(salida, 'w')
  for item in errorStep:
    print>>archivoSalida, item

  #Por greater
  print "GREATER"
  errorClassic = []
  errorStep = []
  for p in (20, 40, 60, 80, 100):
    aEstimator = estimators.ClassicHistogram(archivo, 'datos', 'c1', p)
    bEstimator = estimators.DistributionSteps(archivo, 'datos', 'c1', p)
    bd = InterfazBD(archivo)
    errorA = 0
    errorB = 0
    for i in range(1,101):
      consulta = "select count(c1) from datos where c1>%d" %(i)
      real = bd.realizar_consulta(consulta).fetchone()[0]/float(10000)
      estimadoA = aEstimator.estimate_greater(i)
      estimadoB = bEstimator.estimate_greater(i)
      errorA = errorA + abs(real - estimadoA)
      errorB = errorB + abs(real - estimadoB)
    totalA = errorA / 100
    totalB = errorB / 100
    errorClassic.append((p,totalA))
    errorStep.append((p,totalB))
  salida = archivo + ".greatClassic.txt"
  archivoSalida = open(salida, 'w')
  for item in errorClassic:
    print>>archivoSalida, item
  salida = archivo + ".greatStep.txt"
  archivoSalida = open(salida, 'w')
  for item in errorStep:
    print>>archivoSalida, item


if __name__ == "__main__":
  #  main(sys.argv[1:])
  process("normal.sqlite3")
  process("uniforme.sqlite3")
