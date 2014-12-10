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

# Perfecto
aEstimator = estimators.EstimadorPerfecto('db.sqlite3', 'table1', 'c1', parametro=20)
print "EstimadorPerfecto"
print "  Sel(=%d) : %3.2f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (70, aEstimator.estimate_greater(70))