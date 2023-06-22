# Script το οποιο αποθηκευει τα δεδομενα που εισαγουν οι χρηστες για μελλοντικη χρηση τους στο training dataset
# 1) Θα παίρνει ένα dictionary
# 2) Θα το μετατρεπει σε DataFrame
# 3) Θα το αποθηκευει στο db.xlsx

import pandas as pd
import openpyxl

def saveData(data_list):
        cols = ["Dwelling","Household m2","Bedrooms","Years","Heating Source","Area Code","Occupants",	
            "Children","Teenagers","Adults","Elders","Fulltimers","Parttimers","Grads","PostGrads","Income",
            "Recycling","Energy Class","Thermostats","Water Heater","Smart Plugs","Awareness",	
            "Start","End","Days","Kwhs"]


        df = pd.DataFrame([data_list], columns=cols)

        # df.to_excel("excel/db.xlsx") # For first run time


        excel_reader = pd.ExcelFile('excel/db.xlsx')
        to_update = {"Sheet1": df}

        excel_writer = pd.ExcelWriter('excel/db.xlsx')

        for sheet in excel_reader.sheet_names:
            sheet_df = excel_reader.parse(sheet)
            append_df = to_update.get(sheet)

            if append_df is not None:
                sheet_df = pd.concat([sheet_df, df]).drop_duplicates()

            sheet_df.to_excel(excel_writer, sheet, index=False)

        excel_writer.save()
  
