import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
from sklearn import metrics
import sklearn.metrics as sm
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

from editNo import editing_features_training

X1, y1 = editing_features_training()

X = X1
y = y1

# Polynomial Regression 
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
X_train_poly, X_test_poly, y_train_poly, y_test_poly = train_test_split(X,y, test_size=0.33, random_state=6)

poly = PolynomialFeatures(degree=1)

poly.fit_transform(X_train_poly, y_train_poly)
poly.fit_transform(X_test_poly, y_test_poly)

model = linear_model.LinearRegression()

model.fit(X_train_poly, y_train_poly)

linreg = LinearRegression()

linreg.fit(X_train_poly,y_train_poly)

y_pred = linreg.predict(X_test_poly)

print(f"Score is -->> {r2_score(y_test_poly, y_pred)}")

# --- Save model
pickle.dump(model, open("pickle/polyModelNo.pkl", "wb"))