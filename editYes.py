## ! BE CAREFUL ! 
# This script py use it for 'modelYes.py' script

# -------------------------->
# NOTES
# SOS SOS SOS
# Have very low score this model (-0.04) try to solve this problem
# <--------------------------

def editing_features_training():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import statsmodels.formula.api as smf
    from sklearn import metrics
    import sklearn.metrics as sm


    # Καθαρίσαμε τα δεδομένα της βάσης μας ώστε να έχουμε τα ονόματα των χαρακτηριστικλων που θέλουμε
    cols = ["Dwelling","Dwelling Grade","Household m2","Size Grade","Bedrooms","Years","Old","Heating Source","Area Code","Occupants",	
            "Children","Teenagers","Adults","Elders","Ainc","Adec","Agauge","Fulltimers","Parttimers","Grads","PostGrads",
            "Education Index","Income","Recycling","Energy Class","Thermostats","Water Heater","Smart Plugs","Awareness",	
            "Start","End","Days","Kwhs","Kwh/day","Kwh/day/m2"]
        
    # path = '/content/Data Sheet Energy.xlsx'
    # data = pd.read_csv(path,usecols=cols,skiprows=1)
    data = pd.read_excel('excel/exYes.xlsx')

    train0 = data.drop(columns=['Dwelling', 'Household m2', 'Years', 'Occupants', 'Children', 'Teenagers', 'Adults',
                                'Elders', 'Start', 'End', 'Days', 'Kwhs', 'Kwh/day'])

    df = train0

    # -- FEATURE TRANSFORMATION --
    df1 = df

    # Use ordinal encoding to encode our column
    import category_encoders as ce
    from sklearn.preprocessing import OrdinalEncoder

    sc = ['Rarely', 'Sometimes', 'Often or Always']
    sc1 = ['0 - 10,000€', '10,001€ - 20,000€', '20,001€ - 40,000€', '40,000€ - 60,000€', 'άνω των 60,0001€']

    ordi = OrdinalEncoder(categories=[sc, sc, sc, sc, sc])
    ordi1 = OrdinalEncoder(categories=[sc1])

    ordi.fit(df[['Recycling', 'Energy Class', 'Thermostats', 'Smart Plugs', 'Awareness']])
    ordi1.fit(df[['Income']])

    new_df = ordi.transform(df[['Recycling', 'Energy Class', 'Thermostats', 'Smart Plugs', 'Awareness']])
    new_df = pd.DataFrame(new_df,
                        columns=['Recycling',
                                'Energy Class',
                                'Thermostats',
                                'Smart Plugs',
                                'Awareness'])

    df1['Recycling'] = new_df['Recycling']
    df1['Energy Class'] = new_df['Energy Class']
    df1['Thermostats'] = new_df['Thermostats']
    df1['Smart Plugs'] = new_df['Smart Plugs']
    df1['Awareness'] = new_df['Awareness']
    df1['Income'] = ordi1.transform(df1[['Income']])


    one_hot_encoded_data = pd.get_dummies(df1, columns = ['Water Heater'])
    one_hot_encoded_data = one_hot_encoded_data.drop(columns=['Water Heater_No'])
    df1 = one_hot_encoded_data


    # ---- TARGET ----
    target = df1['Kwh/day/m2']
    df1 = df1.drop(columns=['Kwh/day/m2'])


    # ------ TARGET ENCODING ---
    df_en = df1

    import category_encoders as ce

    tenc=ce.TargetEncoder() 
    df_HS=tenc.fit_transform(df_en['Heating Source'],df_en['Area Code'])

    # Concert df_HS from dataframe to seri and replace this serie with 'Heating Source' serie
    # ser = df_HS.iloc[:,0]

    # print("Type from 'ser'")
    # print(ser)

    # Adding new 'Heating Source' column (with float values) at first column in df_en dataframe
    df_new = df_HS.join(df_en.drop('Heating Source',axis=1))
    df_en = df_new

    # print("DataFrame")
    # print(pd.DataFrame(df_en))

    # Delete column with name 'Unnamed: 0' from df_en dataframe
    df_final = df_en.drop(columns=['Unnamed: 0'])
    df1 = df_final

    # Sorting columns in our dataframe with their names
    # new_cols = ['Dwelling Grade', 'Size Grade', 'Bedrooms', 'Old', 'Heating Source', 
    #                                     'Area Code', 'Ainc', 'Adec', 'Agauge', 'Fulltimers',
    #                                     'Parttimers', 'Grads', 'PostGrads', 'Education Index',
    #                                     'Income', 'Recycling', 'Energy Class', 'Thermostats',
    #                                     'Smart Plugs', 'Awareness', 'Water Heater_Yes']
    # df1=df1.reindex(columns=new_cols)

    # print("New df1 is -> ")
    # print(pd.DataFrame(df1))



    # --- SCALING ---
    from sklearn.datasets import load_iris
    from sklearn.preprocessing import StandardScaler

    object= StandardScaler()

    i_data = df1
    response = target

    # standardization 
    scale = object.fit_transform(i_data) 

    new_df1 = pd.DataFrame(scale, columns=['Dwelling Grade', 'Size Grade', 'Bedrooms', 'Old', 'Heating Source', 
                                        'Area Code', 'Ainc', 'Adec', 'Agauge', 'Fulltimers',
                                        'Parttimers', 'Grads', 'PostGrads', 'Education Index',
                                        'Income', 'Recycling', 'Energy Class', 'Thermostats',
                                        'Smart Plugs', 'Awareness', 'Water Heater_Yes'])


    # --- MISSING VALUES ---
    df1['Bedrooms']=df1['Bedrooms'].fillna(df1['Bedrooms'].mean())


    # --- DELETE SOME FEATURES ---
    df1 = df1.drop(columns=['Ainc', 'Adec', 'Grads', 'PostGrads', 'Education Index',
                            'Smart Plugs', 'Awareness'])


    # print("Traing transformation data ")
    # print(df1)


    X_array_train = np.array(df1)
    y_array_train = np.array(target)

    return X_array_train, y_array_train



# -----------------------------------------------------

# --------- Feature Test Transformation ---------------

def convert_to_dict(list_features):
    keys = ["Dwelling", "Household m2","Bedrooms", "Years", "Heating Source", "Area Code","Income",
            "Water Heater","Occupants", "Children", "Teenagers", "Adults", "Elders",
            "Fulltimers","Parttimers","Grads","PostGrads","Recycling","Energy Class","Thermostats","Smart Plugs",
            "Awareness","Start","End","Days","Kwhs"]

    dictionary_features = dict(zip(keys,list_features))
    return dictionary_features


# θα καλειται τελευταια
# def delete_non_important_features(dict_features):
#     new_dict = dict_features
#     remove_list = ['Dwelling', 'Household m2', 'Years', 'Occupants', 'Children', 'Teenagers', 'Adults',
#                                 'Elders', 'Start', 'End', 'Days', 'Kwhs']
                
#     [new_dict.pop(key) for key in remove_list]
#     return new_dict



def dwelling_grade_fun(dwelling_object):
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
    size_grade_object = int(size_grade_object)

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


#Τα strinf "0-5" να μην εχουν κενα
def old_fun(old_object):
    if old_object == "0-5":
        old_var = 0.0
    elif old_object == "6-15":
        old_var = 0.33
    elif old_object == "16-30":
        old_var = 0.66
    else:
        old_var = 1.0
    return old_var

def ainc_fun(children, teenager, adult, eider):
    children = int(children)
    teenager = int(teenager)
    adult = int(adult)
    eider = int(eider)

    ainc_var = (0.5 * children) + (0.75 * teenager) + (0.9 * adult) + (1.0 * eider)
    return ainc_var

def adec_fun(children, teenager, adult, eider):
    children = int(children)
    teenager = int(teenager)
    adult = int(adult)
    eider = int(eider)

    adec_var = (1.0 * children) + (0.9 * teenager) + (0.75 * adult) + (0.5 * eider)
    return adec_var

def aga_fun(children, teenager, adult, eider):
    children = int(children)
    teenager = int(teenager)
    adult = int(adult)
    eider = int(eider)

    aga_var = (0.5 * children) + (0.75 * teenager) + (1.0 * adult) + (0.5 * eider)
    return aga_var

# BE CAREFULLY FOR MATHEMATIC TYPE !!!!!!!!!!!!!!!!!!
def edu_fun(children, teenager, grads, postg):
    children = int(children)
    teenager = int(teenager)
    grads = int(grads)
    postg = int(postg)

    EYS = 17.91 * (children + teenager)
    MYS = (4 * grads) + (6 * postg)
    
    EI = ( (EYS + MYS ) / 18 ) / 2

    return EI



def oridinal_encode_fun(feature1, feature2, feature3, feature4, feature5, feature6, dict):
    # ----- Ordinal Encoding -----
    # rarely -> 0.0
    # sometimes -> 1.0
    # oftena or always -> 2.0

    list_names = [feature1,feature2,feature3,feature4,feature5]

    for name in list_names:
        if dict[name] == 'Rarely':
            dict[name] = 0.0
        elif dict[name] == 'Sometimes':
            dict[name] = 1.0
        else:
            dict[name] = 2.0 

    # ----------
    # ----- Ordinal Encoding for 'Heating Source' and 'Water Heater' -----  
    # Yes -> 1.0
    # No -> 0.0

    if dict['Water Heater'] == 'Yes':
        dict['Water Heater'] = 1.0
    else:
        dict['Water Heater'] = 0.0


    if dict['Heating Source'] == 'Yes':
        dict['Heating Source'] = 1.0
    else:
        dict['Heating Source'] = 0.0


    # Encode 'Income'
    # '0 - 10,000€' -> 0.0
    # '10,001€ - 20,000€' -> 1.0
    # '20,001€ - 40,000€' -> 2.0
    # '40,000€ - 60,000€' -> 3.0
    # 'άνω των 60,0001€' -> 4.0
    if dict['Income'] == '0 - 10,000€':
        dict['Income'] = 0.0
    elif dict['Income'] == '10,001€ - 20,000€':
        dict['Income'] = 1.0
    elif dict['Income'] == '20,001€ - 40,000€':
        dict['Income'] = 2.0
    elif dict['Income'] == '40,000€ - 60,000€':
        dict['Income'] = 3.0
    else:
        dict['Income'] = 4.0
    
    
    return dict

   

# example_dict = {'Dwelling': 'Family House', 'Years': '0-5', 
# 'Heating Source': 'Yes', 'Income': '20,001€ - 40,000€', 'Recycling': 'Rarely', 'Energy Class': 'Rarely', 
# 'Thermostats': 'Rarely', 'Smart Plugs': 'Often or Always', 'Awareness': 'Sometimes', 'Water Heater': 'Yes', 
# 'Household m2': '200', 'Bedrooms': '10', 'Area Code': '1267', 'Occupants': '2', 'Children': '2', 
# 'Teenagers': '6', 'Adults': '4', 'Elders': '2', 'Fulltimers': '2', 'Parttimers': '2', 'Grads': '2',
# 'PostGrads': '2', 'Start': '12', 'End': '12', 'Days': '365', 'Kwhs': '1233'}


def editing_features_test(feature_dict):
    result_dict = {}
    result_dict['Dwelling Grade'] = dwelling_grade_fun(feature_dict['Dwelling'])
    result_dict['Size Grade'] = size_grade_fun(feature_dict['Household m2'])
    result_dict['Bedrooms'] = float(feature_dict['Bedrooms'])
    result_dict['Old'] = old_fun(feature_dict['Years'])
    result_dict['Heating Source'] = feature_dict['Heating Source']
    result_dict['Area Code'] = float(feature_dict['Area Code'])
    result_dict['Ainc'] = ainc_fun(feature_dict['Children'], feature_dict['Teenagers'], feature_dict['Adults'], feature_dict['Elders'])
    result_dict['Adec'] = adec_fun(feature_dict['Children'], feature_dict['Teenagers'], feature_dict['Adults'], feature_dict['Elders'])
    result_dict['Agauge'] = aga_fun(feature_dict['Children'], feature_dict['Teenagers'], feature_dict['Adults'], feature_dict['Elders'])
    result_dict['Fulltimers'] = float(feature_dict['Fulltimers'])
    result_dict['Parttimers'] = float(feature_dict['Parttimers'])
    result_dict['Grads'] = float(feature_dict['Grads'])
    result_dict['PostGrads'] = float(feature_dict['PostGrads'])
    result_dict['Education Index'] = edu_fun(feature_dict['Children'], feature_dict['Teenagers'], feature_dict['Grads'], feature_dict['PostGrads'])
    result_dict['Income'] = feature_dict['Income']
    result_dict['Recycling'] = feature_dict['Recycling']
    result_dict['Energy Class'] = feature_dict['Energy Class']
    result_dict['Thermostats'] = feature_dict['Thermostats']

    # result_dict['Heating Source'] = feature_dict['Heating Source'] # new new new
    
    result_dict['Water Heater'] = feature_dict['Water Heater']
    result_dict['Smart Plugs'] = feature_dict['Smart Plugs']
    result_dict['Awareness'] = feature_dict['Awareness']


    # Encoding Features
    result_dict = oridinal_encode_fun('Recycling','Energy Class', 'Thermostats','Smart Plugs','Awareness','Income', result_dict)

    # Delete some not so importan keys
    # θα καλειται η αντιστοιχη συναρτηση που εχουμε παραπανω
    del result_dict['Ainc']
    del result_dict['Adec']
    del result_dict['Grads']
    del result_dict['PostGrads']
    del result_dict['Education Index']
    del result_dict['Smart Plugs']
    del result_dict['Awareness']


    result_list = list(result_dict.values())


    return result_list


# example = editing_features_test(example_dict)
# print(example)
