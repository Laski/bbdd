import matplotlib.pyplot as plt
import numpy
from interfazbd import InterfazBD
import estimators as est
import empirico
from scipy import stats

def graficar_dataset(nombre_bd, tabla, columna):
	plt.clf()
	bd = InterfazBD(nombre_bd)
	values = list(bd.consultar(tabla, columna, ""))
	values = [v for (v,) in values]
	plt.hist(values, 200)
	plt.ylabel("Valor")
	plt.xlabel("Cantidad" + " (" + nombre_bd + " - " + tabla + " - " + columna + ")")
	archivo = "datasets/img/" + columna + ".png"
	plt.savefig(archivo)

def graficar_datasets_catedra():
	for i in range(0,10):
		graficar_dataset("db.sqlite3", "table1", "c"+str(i))

def rango(nombre_bd, tabla, columna):
	bd = InterfazBD(nombre_bd)
	consulta_min_max = "SELECT %s(" + columna + ") FROM (SELECT " + columna + " FROM " + tabla + " GROUP BY " + columna + ")"
	minimo = list(bd.realizar_consulta(consulta_min_max % "MIN"))[0][0]
	maximo = list(bd.realizar_consulta(consulta_min_max % "MAX"))[0][0]
	return minimo, maximo
	
def diferencias_performance():
	bd = "db.sqlite3"
	tabla = "table1"
	res = []
	for i in range(0,10):
		col = "c"+str(i)
		#print i
		p_equal, p_greater = ttest_estimadores(bd, tabla, col)
		#print (p_equal, p_greater)
		res.append((p_equal, p_greater))		
	return res

def ttest_estimadores(bd, tabla, col):
	
	#inicializar estimadores
	est1 = est.ClassicHistogram(bd, tabla, col)
	est2 = est.DistributionSteps(bd, tabla, col)		
	est_perfecto = est.EstimadorPerfecto(bd, tabla, col)
	
	min, max = rango(bd, tabla, col)
	
	#calcular performances intermedias
	perf1_equal = empirico.calcular_performances_intermedias(est1.estimate_equal, est_perfecto.estimate_equal, range(min, max, 10))
	perf2_equal = empirico.calcular_performances_intermedias(est2.estimate_equal, est_perfecto.estimate_equal, range(min, max, 10))		
	perf1_greater = empirico.calcular_performances_intermedias(est1.estimate_greater, est_perfecto.estimate_greater, range(min, max, 10))
	perf2_greater = empirico.calcular_performances_intermedias(est2.estimate_greater, est_perfecto.estimate_greater, range(min, max, 10))
	
	#hacer el ttest
	_, p_equal = stats.ttest_rel(perf1_equal, perf2_equal)
	_, p_greater = stats.ttest_rel(perf1_greater, perf2_greater)
	
	return p_equal, p_greater

if __name__ == "__main__":
	graficar_datasets_catedra()
	print(diferencias_performance())
