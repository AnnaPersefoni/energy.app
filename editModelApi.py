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

def feature_transformation(df):
    df1 = df

    sc = ['Rarely', 'Sometimes', 'Often or Always']
    sc1 = ['0 - 10,000€', '10,001€ - 20,000€', '20,001€ - 40,000€', '40,000€ - 60,000€', 'άνω των 60,0001€']

    ordi = OrdinalEncoder(categories=[sc, sc, sc])
    ordi1 = OrdinalEncoder(categories=[sc1])

    ordi.fit(df[['Recycling', 'Energy Class', 'Thermostats']])
    ordi1.fit(df[['Income']])

    new_df = ordi.transform(df[['Recycling', 'Energy Class', 'Thermostats']])
    new_df = pd.DataFrame(new_df,
                        columns=['Recycling',
                                'Energy Class',
                                'Thermostats',])


    df1['Recycling'] = new_df['Recycling']
    df1['Energy Class'] = new_df['Energy Class']
    df1['Thermostats'] = new_df['Thermostats']

    df1['Income'] = ordi1.transform(df1[['Income']])


    # Hot Encoding!
    one_hot_encoded_data = pd.get_dummies(df1, columns = ['Heating Source', 'Water Heater'])
    # one_hot_encoded_data.tail(2)
    one_hot_encoded_data = one_hot_encoded_data.drop(columns=['Heating Source_No', 'Water Heater_No'])
    df1 = one_hot_encoded_data

    return df1




def dwelling_grade(dwelling_object):
    if dwelling_object == "Appartment":
        dwelling_grade_var = 0.0
    elif dwelling_object == "Townhome":
        dwelling_grade_var = 0.4
    elif dwelling_object == "Semidetached":
        dwelling_grade_var = 0.7
    else:
        dwelling_grade_var = 1.0
    return dwelling_grade_var


def size_grade_fun(size_grade_object):
    # size_grade_object = int(size_grade_object)

    if size_grade_object >= 0 and size_grade_object <= 60:
        size_grade_var = 0.0
    elif size_grade_object >= 61 and size_grade_object <= 80:
        size_grade_var = 0.2
    elif size_grade_object >= 81 and size_grade_object <= 100:
        size_grade_var = 0.4
    elif size_grade_object >= 101 and size_grade_object <= 140:
        size_grade_var = 0.6
    elif size_grade_object >= 141 and size_grade_object <= 200:
        size_grade_var = 0.8
    else:
        size_grade_var = 1.0
    return size_grade_var 

def get_old(built):
    old = 2023 - built
    return old


def aga_fun(children, teenager, adult, eider):
    children = int(children)
    teenager = int(teenager)
    adult = int(adult)
    eider = int(eider)



    

def editing_features_training(features_directory):
    new_dictionary = {}

    new_dictionary['Dwelling Grade'] = dwelling_grade(features_directory['Dwelling'])
    new_dictionary['Size Grade'] = size_grade_fun(features_directory['Household m2'])
    new_dictionary['Bedrooms'] = features_directory['Bedrooms']
    new_dictionary['Old'] = get_old(features_directory['built'])
    new_dictionary['Agauge'] = aga_fun(features_directory['Children'],features_directory['Teenagers'],features_directory['Adults'],features_directory['Elders'])
    new_dictionary['Fulltimers'] = features_directory['Fulltimers']
    new_dictionary['Parttimers'] = features_directory['Parttimers']


    del features_directory['Dwelling']
    del features_directory['Household m2']
    del features_directory['Bedrooms']
    del features_directory['built']
    del features_directory['Children']
    del features_directory['Teenagers']
    del features_directory['Adults']
    del features_directory['Elders']
    del features_directory['Fulltimers']
    del features_directory['Parttimers']


    # train0 = df_list.drop(columns=['Income', 'Recycling', 'Thermostats', 'Heating Source_Yes', 'Water Heater_Yes'])

    df_list = []
    df_list.append(features_directory['Income'])
    df_list.append(features_directory['Recycling'])
    df_list.append(features_directory['Energy Class'])
    df_list.append(features_directory['Thermostats'])
    df_list.append(features_directory['Heating Source'])
    df_list.append(features_directory['Water Heater'])

    print(f"Array valuesssssssssssssss")
    print(df_list)

    cols = ['Income', 'Recycling', 'Energy Class', 'Thermostats', 'Heating Source_Yes', 'Water Heater_Yes']
    new_cols = np.reshape(cols, (6,1)).T
    # new_df_list = np.reshape(df_list, (12, 5)).T
    train0 = pd.DataFrame(df_list, columns = new_cols)  

    print(f"DataFrame hereeeeeeeeeeee")
    print(train0)

    transformation_dict = feature_transformation(train0)

    new_dictionary['Income'] = transformation_dict['Income']
    new_dictionary['Recycling'] = transformation_dict['Recycling']
    new_dictionary['Energy Class'] = transformation_dict['Energy Class']
    new_dictionary['Thermostats'] = transformation_dict['Thermostats']
    #Heating_Source and Water_Heater
    new_dictionary['Heating Source_Yes'] = transformation_dict['Heating Source_Yes']
    new_dictionary['Water Heater_Yes'] = transformation_dict['Water Heater_Yes']

    print(f"New directory !!!!!!!!!! ")
    print(new_dictionary)
    

