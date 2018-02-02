from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.externals import joblib
from xgboost import XGBRegressor


class EnsembleRegressor:

    def __init__(self):
        self.rf_regr = RandomForestRegressor(max_depth=2, random_state=0)
        self.gb_regr = GradientBoostingRegressor()
        self.xgb_regr = XGBRegressor(max_depth=10,
                                     learning_rate=0.1,
                                     n_estimators=10,
                                     silent=True,
                                     objective='reg:linear',
                                     nthread=-1,
                                     gamma=0,
                                     min_child_weight=1,
                                     max_delta_step=0,
                                     subsample=0.85,
                                     colsample_bytree=0.7,
                                     colsample_bylevel=1,
                                     reg_alpha=0,
                                     reg_lambda=1,
                                     scale_pos_weight=1,
                                     seed=1440,
                                     missing=None)

    def random_forest(self, feature_matrix, label_matrix):
        self.rf_regr.fit(feature_matrix, label_matrix)

    def gradient_boosting(self, feature_matrix, label_matrix):
        self.gb_regr.fit(feature_matrix, label_matrix)

    def xgboost(self, feature_matrix, label_matrix):
        self.xgb_regr.fit(feature_matrix, label_matrix)

    def save_model(self):
        joblib.dump([self.rf_regr, self.gb_regr, self.xgb_regr], 'regressors.model')
