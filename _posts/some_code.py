import numpy as np

class LinearRegressor:
    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept

    def fit(self, X, y):
        if self.fit_intercept:
            # Append a column of ones to X which accounts for the intercept
            ones_column = np.ones(X.shape[0])[:, np.newaxis]
            X_w_ones = np.column_stack((ones_column, X))

            # Set self.coef_ as the least squares estimator (X'X)^(-1)(X'y)
            self.coef_, _, _, _ = np.linalg.lstsq(X_w_ones, y)

            # Split the coefficients into intercept and non-intercept part
            self.intercept_ = self.coef_[0]
            self.coef_ = self.coef_[1:]
        else:
            # Set self.coef_ as the least squares estimator (X'X)^(-1)(X'y)
            self.coef_, _, _, _ = np.linalg.lstsq(X, y)

        return self

    def predict(self, X):
        if self.fit_intercept:
            return X @ self.coef_ + self.intercept_
        else:
            return X @ self.coef_
