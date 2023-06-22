# Python script which create 2 different ecxel sheets
# -> One script for "Heating Source == 'No' "
# -> One script for "Heating Source == 'Yes' "


import pandas as pd

cols = ["Dwelling","Dwelling Grade","Household m2","Size Grade","Bedrooms","Years","Old","Heating Source","Area Code","Occupants",	
            "Children","Teenagers","Adults","Elders","Ainc","Adec","Agauge","Fulltimers","Parttimers","Grads","PostGrads",
            "Education Index","Income","Recycling","Energy Class","Thermostats","Water Heater","Smart Plugs","Awareness",	
            "Start","End","Days","Kwhs","Kwh/day","Kwh/day/m2"]

df = pd.read_excel('excel/ex.xlsx',usecols=cols,skiprows=1)

import category_encoders as ce
from sklearn.preprocessing import OrdinalEncoder

# -- Delete rows with "Heating Source" == "No"
df_yes_heating_source = df[ df['Heating Source'] == 'No' ] # Step 1
df1 = df.drop(df_yes_heating_source.index, axis=0) # Step 2
df1.to_excel('excel/exYes.xlsx')

df_no_heating_source = df[ df['Heating Source'] == 'Yes' ] # Step 1
df2 = df.drop(df_no_heating_source.index, axis=0) # Step 2
df2.to_excel('excel/exNO.xlsx')
