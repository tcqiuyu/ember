import numpy as np
from traditional.regression import EnsembleRegressor

from utils import *

training_path_base = "../../data/training/"

# Loading features
[traditional_features, label] = pload(training_path_base + "traditional_features.pickle")


ensem_regressor = EnsembleRegressor()
# ensem_regressor.random_forest(traditional_features, label)
# ensem_regressor.gradient_boosting(traditional_features, label)
# ensem_regressor.xgboost(traditional_features, label)
# ensem_regressor.save_model(training_path_base+"regr_model.pickle")
ensem_regressor.load_model(training_path_base+"regr_model.pickle")
