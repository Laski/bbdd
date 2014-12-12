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
    plt.ylabel("Cantidad")
    plt.xlabel("Valor (" + columna + ")")
    archivo = "datasets/img/" + columna + ".png"
    plt.savefig(archivo)


def graficar_datasets_catedra():
    for i in range(0, 10):
        graficar_dataset("datasets/db.sqlite3", "table1", "c"+str(i))


def rango(nombre_bd, tabla, columna):
    bd = InterfazBD(nombre_bd)
    consulta_min_max = "SELECT %s(" + columna + ") FROM (SELECT " + columna + " FROM " + tabla + " GROUP BY " + columna + ")"
    minimo = list(bd.realizar_consulta(consulta_min_max % "MIN"))[0][0]
    maximo = list(bd.realizar_consulta(consulta_min_max % "MAX"))[0][0]
    return minimo, maximo

    
def diferencias_performance(tipo1, tipo2, param):
    print("#########################")
    print(tipo1.title() + " vs " + tipo2.title())
    bd = "datasets/db.sqlite3"
    tabla = "table1"
    res = []
    for i in range(0, 10):
        col = "c"+str(i)
        print col
        
        est1 = get_estimator(tipo1, bd, tabla, col, param)
        est2 = get_estimator(tipo2, bd, tabla, col, param)
        est_perfecto = est.EstimadorPerfecto(bd, tabla, col)
        
        perf1_equal = empirico.calcular_performance_global(est1.estimate_equal, est_perfecto.estimate_equal)
        perf2_equal = empirico.calcular_performance_global(est2.estimate_equal, est_perfecto.estimate_equal)
        perf1_greater = empirico.calcular_performance_global(est1.estimate_greater, est_perfecto.estimate_greater)
        perf2_greater = empirico.calcular_performance_global(est2.estimate_greater, est_perfecto.estimate_greater)
        
        p_equal, p_greater = ttest_estimadores(bd, tabla, col, est1, est2)
        print "Equal:"
        if p_equal >= 0.05:
            print "\tEmpate"
        elif perf1_equal < perf2_equal:
            print "\tGana", tipo1.title(), "(P=" + str(p_equal) + ")"
        else:
            print "\tGana", tipo2.title(), "(P=" + str(p_equal) + ")"
        print "Greater:"
        if p_greater >= 0.05:
            print "\tEmpate"
        elif perf1_greater < perf2_greater:
            print "\tGana", tipo1.title(), "(P=" + str(p_greater) + ")"
        else:
            print "\tGana", tipo2.title(), "(P=" + str(p_greater) + ")"
    print


def get_estimator(tipo, bd, tabla, col, param):
    if tipo == "classic":
        return est.ClassicHistogram(bd, tabla, col, param)
    elif tipo == "steps":
        return est.DistributionSteps(bd, tabla, col, param)
    elif tipo == "propio":
        return est.EstimadorGrupo(bd, tabla, col, param)


def ttest_estimadores(bd, tabla, col, est1, est2):
    #inicializar estimadores        
    est_perfecto = est.EstimadorPerfecto(bd, tabla, col)
    
    minimo, maximo = rango(bd, tabla, col)
    
    #calcular performances intermedias
    perf1_equal = empirico.calcular_performances_intermedias(est1.estimate_equal, est_perfecto.estimate_equal, range(minimo, maximo, 10))
    perf2_equal = empirico.calcular_performances_intermedias(est2.estimate_equal, est_perfecto.estimate_equal, range(minimo, maximo, 10))        
    perf1_greater = empirico.calcular_performances_intermedias(est1.estimate_greater, est_perfecto.estimate_greater, range(minimo, maximo, 10))
    perf2_greater = empirico.calcular_performances_intermedias(est2.estimate_greater, est_perfecto.estimate_greater, range(minimo, maximo, 10))
    
    #hacer el ttest
    _, p_equal = stats.ttest_rel(perf1_equal, perf2_equal)
    _, p_greater = stats.ttest_rel(perf1_greater, perf2_greater)
    
    return p_equal, p_greater


if __name__ == "__main__":
    #graficar_datasets_catedra()
    diferencias_performance("classic", "steps", 100)
    diferencias_performance("classic", "propio", 100)
    diferencias_performance("steps", "propio", 100)
