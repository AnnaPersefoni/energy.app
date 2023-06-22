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

# ----- Linear Regression -----

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=6)

model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)

print(f"Prediction is -> {pred}")

score_test = model.score(X_test, y_test)

print(f"Score is -> : {score_test}")

# ---------------------------

pickle.dump(model, open("pickle/modelNo.pkl", "wb"))
