import requests


def convert_to_int(string):
    new_integer = float(string)
    return new_integer




def request_api():
    path = "http://lavoro.csd.auth.gr:8000/dev_id/emon_4c5bc44b/meta/?field="
    key1 = "Household m2"

    featuresArr = []
    featuresArr.append("name")
    featuresArr.append("Household m2")
    featuresArr.append("Dwelling")
    featuresArr.append("Bedrooms")
    featuresArr.append("built")
    featuresArr.append("Heating Source")
    featuresArr.append("Income")
    featuresArr.append("Water Heater")
    featuresArr.append("Occupants")
    featuresArr.append("Children")
    featuresArr.append("Teenagers")
    featuresArr.append("Adults")
    featuresArr.append("Elders")
    featuresArr.append("Fulltimers")
    featuresArr.append("Parttimers")
    featuresArr.append("Grads")
    featuresArr.append("PostGrads")
    featuresArr.append("Recycling")
    featuresArr.append("Energy Class")
    featuresArr.append("Thermostats")
    featuresArr.append("Smart Plugs")
    featuresArr.append("Awareness")


    featuresDict = {}

    for feature in featuresArr:
        req = path+feature
        response = requests.get(req)
        result = response.json()


        if type(result) == dict:
            featuresDict[feature] = ""
        else:
            featuresDict[feature] = result

        
        # if result.isnumeric() == True:
        #     new_result = convert_to_int(result)
        #     featuresDict[feature] = new_result
        # else:
        #     featuresDict[feature] = result


    return featuresDict


