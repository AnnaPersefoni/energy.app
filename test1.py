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
import category_encoders as ce
from sklearn.preprocessing import OrdinalEncoder



def get_years(built):
    years = 2023 - built
    return years


def first_test(features_dict):
    # print(f"Type from features_dict")
    # print(features_dict)

    new_dict = {}
    new_dict['Dwelling'] = features_dict['Dwelling']
    new_dict['Household m2'] = features_dict['Household m2']
    new_dict['Bedrooms'] = features_dict['Bedrooms']
    new_dict['Years'] = get_years(features_dict['built'])
    new_dict['Heating Source'] = features_dict['Heating Source']
    new_dict['Area Code'] = 0
    new_dict['Occupants'] = features_dict['Occupants']
    new_dict['Children'] = features_dict['Children']
    new_dict['Teenagers'] = features_dict['Teenagers']
    new_dict['Adults'] = features_dict['Adults']
    new_dict['Elders'] = features_dict['Elders']
    new_dict['Fulltimers'] = features_dict['Fulltimers']
    new_dict['Parttimers'] = features_dict['Parttimers']
    new_dict['Grads'] = features_dict['Grads']
    new_dict['PostGrads'] = features_dict['PostGrads']
    new_dict['Income'] = features_dict['Income']
    new_dict['Recycling'] = features_dict['Recycling']
    new_dict['Energy Class'] = features_dict['Energy Class']
    new_dict['Thermostats'] = features_dict['Thermostats']
    new_dict['Water Heater'] = features_dict['Water Heater']
    new_dict['Smart Plugs'] = features_dict['Smart Plugs']
    new_dict['Awareness'] = features_dict['Awareness']


    # print(f"RESULT DICTIONARY")
    # print(new_dict)

    return new_dict














