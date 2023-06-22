from flask import Flask, render_template, request, url_for
import os
from flask import send_from_directory
import pandas as pd
import pickle
import numpy as np

from editNo import convert_to_dict, editing_features_test
from saveNewData import saveData
from calcDays import num_days

from apiManager import convert_to_int, request_api
import requests
 
from editModelApi import editing_features_training

# FOR TESTING
from test1 import first_test, get_years

def convert_to_int(string):
    new_integer = float(string)
    return new_integer


app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')
modelNo = pickle.load(open("pickle/modelNo.pkl", "rb"))

modelYes = pickle.load(open("pickle/model.pkl", "rb")) # THIS  
# modelYes = pickle.load(open("pickle/modelYes.pkl", "rb")) # Βγαζει πολλες μηδενικες τιμες
# modelYes = pickle.load(open("modelYesPoly.pkl", "rb"))

polyModelNo = pickle.load(open("pickle/polyModelNo.pkl", "rb")) # polynomial regression model


@app.route("/")
def intro():
    return render_template("login.html")

@app.route("/form_login", methods=["POST", "GET"])
def login():
    return render_template("choosePage.html")

@app.route("/choose_form", methods=["POST", "GET"])
def choosing():

    choise = [c for c in request.form.values()]

    print(choise)

    if choise[0] == "menu":
        return render_template("home.html")
    else:
        return render_template("apiPage.html")

@app.route("/api_form", methods=["POST", "GET"])
def resultApi():


    # ** NOTES **
    # Να αλλαχθουν τα ονοματα των features γιατι ειναι διαφορετικα με αυτα που εχω
    # Επειτα να βαλω στο μοντελο το dictionary με τα features
    # Να παρω το αποτελεσμα του μοντελου και αναλογα την καταναλωση να 
    # -> να εμφανιζω μηνυμα για το ενεργειακο αποτυπωμα του σπιτιου

    featuresDict = {}
    featuresDict = request_api()


    # print(f"Print request dictionary")
    # print(featuresDict)

    # editing_features_training(featuresDict)

    # FOR TESTING 
    # AFTER TESTING MUST DELETE IT

    df = first_test(featuresDict)
    kwhs = 0.10

    final_features = editing_features_test(df)

    data = np.array(final_features)
    data1 = data.reshape(1,-1)

    heating_source_value = df['Heating Source']

    if heating_source_value == 'No' or not(heating_source_value):
        pred1 = modelNo.predict(data1)
        print("IN No")
        # pred1 = polyModelNo.predict(data1)
    else:
        print("IN YES")
        # Να κανω testing με τιμες 'Heating Source' = 'Yes' 
        pred1 = modelYes.predict(data1)


    if kwhs > pred1:
        d1 = kwhs - pred1

        d1 = np.round(d1,4)
        pred1 = np.round(pred1,4)

        edit_user_kwhs = np.round(kwhs,4)
        return render_template("messageUp.html", diafora=d1, result=pred1, user_kwhs=edit_user_kwhs)
    else:
        d2 = pred1 - kwhs

        d2 = np.round(d2,4)
        pred1 = np.round(pred1,4)

        edit_user_kwhs = np.round(kwhs,4)
        return render_template("messageDown.html", diafora=d2, result=pred1, user_kwhs=edit_user_kwhs)


            
    return render_template("apiResult.html", size_value=featuresDict['Household m2'], income=featuresDict['Income']) 

@app.route("/form_home", methods=["POST", "GET"])
def home():

    features1 = [x for x in request.form.values()]

    new_features = convert_to_dict(features1)

    print(f"new_features -> {new_features}")

    # ------ Save 'Kwhs' from user input ------
    kwhs = float(new_features['Kwhs'])
    # Διαγραφω το πεδιο 'Kwhs' απο το dictionary "new_features"
    new_features.popitem()
    # -------------------------------------------


    # ------ Save 'Days' from app script ------
    days = num_days(new_features['Start'], new_features['End'])


    # Add 'Days' field in "feaures" list because we want save and days in our database
    features1.insert(len(features1)-1,days)

    # -----
    saveData(features1) #Save user input data in database (excel file)
    # -----

    print(f"Num days is : {days}")
    
    final_features = editing_features_test(new_features)

    data = np.array(final_features)
    data1 = data.reshape(1,-1)


    heating_source_value = new_features['Heating Source']
    
    if heating_source_value == 'No':
        pred1 = modelNo.predict(data1)
        # pred1 = polyModelNo.predict(data1)
    else:
        # Να κανω testing με τιμες 'Heating Source' = 'Yes' 
        pred1 = modelYes.predict(data1)


    m2 = float(new_features['Household m2'])
    res = ((pred1 / days) / m2)
    # print(f"Predict is -> {res}")

    # Υπολογιζουμε kwhs/day/m2 που εισηγατε ο χρηστης
    kdm = (kwhs / days) / m2

    # Ελεγχουμε αν καταναλωθηκαν περισσοτερες kwhs/day/m2 απο τις προβλεπομενες του μοντελου
    if kdm > res:
        d1 = kdm - res

        d1 = np.round(d1,4)
        res = np.round(res,4)

        edit_user_kwhs = np.round(kdm,4)
        return render_template("messageUp.html", diafora=d1, result=res, user_kwhs=edit_user_kwhs)
    else:
        d2 = res - kdm

        d2 = np.round(d2,4)
        res = np.round(res,4)

        edit_user_kwhs = np.round(kdm,4)
        return render_template("messageDown.html", diafora=d2, result=res, user_kwhs=edit_user_kwhs)




if __name__ == '__main__':
    app.run(debug=True)




# ----------------- NOTES -------------------------------------

#  TΙ ΠΡΕΠΕΙ ΝΑ ΚΑΝΩ
#
# [1*] Να κανω Polynomial regression και για το μοντελο modelYes
# [2*] Να σβησω τα πεδια που ΔΕΝ χρησιμοποιω (πχ 'Awareness')
# [3*] Να δω για outliers που δεν ελενξα



#  ΤΙ ΕΧΩ ΚΑΝΕΙ
#
# [1*] Εκανα script που παιρνει 2 ημερομηνιες και υπολογιζει τον αριθμο των ημερων που αντιστοιχουν
# [2*] Σκεφτηκα να αφησω ολα τα πεδια στο "home page" διοτι μπορει μελλοντικα να γινουν αλλαγες στα 
#      πεδια που χρησιμοποιουμε για την εκπαιδευση του μοντελου
