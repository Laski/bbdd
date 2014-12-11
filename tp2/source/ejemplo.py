# -*- coding: utf-8 -*-

import estimators

# ClassicHistogram
aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', 'c1', parametro=20)
print "ClassicHistogram"
print "  Sel(=%d) : %3.2f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (70, aEstimator.estimate_greater(70))

# DistributionSteps
aEstimator = estimators.DistributionSteps('db.sqlite3', 'table1', 'c1', parametro=20)
print "DistributionSteps"
print "  Sel(=%d) : %3.2f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (70, aEstimator.estimate_greater(70))

#Grupo
aEstimator = estimators.EstimadorGrupo('db.sqlite3', 'table1', 'c1', parametro=20)
print "Estimador Grupo"
print "  Sel(=%d) : %3.2f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (60, aEstimator.estimate_greater(60))


# Perfecto
aEstimator = estimators.EstimadorPerfecto('db.sqlite3', 'table1', 'c1', parametro=20)
print "EstimadorPerfecto"
print "  Sel(=%d) : %3.2f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (70, aEstimator.estimate_greater(70))

#Para base de muchos repetidos
# ClassicHistogram
print '########################'
aEstimator = estimators.ClassicHistogram('raro.sqlite3', 'datos', 'c', parametro=20)
print "ClassicHistogram"
print "  Sel(=%d) : %3.2f" % (16, aEstimator.estimate_equal(16))
print "  Sel(>%d) : %3.2f" % (400, aEstimator.estimate_greater(400))

# DistributionSteps
aEstimator = estimators.DistributionSteps('raro.sqlite3', 'datos', 'c', parametro=20)
print "DistributionSteps"
print "  Sel(=%d) : %3.2f" % (16, aEstimator.estimate_equal(16))
print "  Sel(>%d) : %3.2f" % (400, aEstimator.estimate_greater(400))

#Grupo
aEstimator = estimators.EstimadorGrupo('raro.sqlite3', 'datos', 'c', parametro=20)
print "Estimador Grupo"
print "  Sel(=%d) : %3.2f" % (16, aEstimator.estimate_equal(16))
print "  Sel(>%d) : %3.2f" % (400, aEstimator.estimate_greater(400))

# Perfecto
aEstimator = estimators.EstimadorPerfecto('raro.sqlite3', 'datos', 'c', parametro=20)
print "EstimadorPerfecto"
print "  Sel(=%d) : %3.2f" % (16, aEstimator.estimate_equal(16))
print "  Sel(>%d) : %3.2f" % (400, aEstimator.estimate_greater(400))
