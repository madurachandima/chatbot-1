import json

def get_illness(symptoms_array=[]):
    print(symptoms_array)
    # symptoms_array = [
    #     {"fever": "no"},
    #     {"diarrhea": "no"},
    #     {"vomiting": "no"},
    #     {"reduced_appetite": "yes"},
    #     {"dehydration": "no"},
    #     {"leathargy": "no"},
    #     {"Increased_urination": "NO"},
    #     {"Weight_loss": "no"},
    #     {"skin_infections": "no"},
    #     {"labored_breathing": "NO"},
    #     {"runny_eyes": "NO"},
    #     {"coughing": "NO"},
    #     {"paralysis": "no"},
    #     {"limping": "no"}]

    illnesses_array = []

    try:
        intents = ""
        with open('symptoms_db.json', 'r') as f:
            intents = json.load(f)

            for symptom_array in symptoms_array:
                key = ""
                value = ""
                for k, v in symptom_array.items():
                    key = str(k).upper()
                    value = str(v).upper()

                for intent in intents['intents']:
                    for symptom in intent['symptoms']:
                        # print(symptom)
                        s_key = ""
                        s_value = ""
                        for s_k, s_v in symptom.items():
                            s_key = str(s_k).upper()
                            s_value = str(s_v).upper()
                        # print(s_key, s_value)
                        if key == s_key and value == s_value:
                            illnesses_array.append(intent['responses'])
                        else:
                            try:
                                if any(element in intent['responses'] for element in illnesses_array):
                                    illnesses_array.remove(intent['responses'])
                            except Exception as e:
                                print(e)
            if len(illnesses_array) == 1:
                return illnesses_array[0]
                print(illnesses_array)
            else:
                print("No result found")
                return "No result found"
            illnesses_array.clear()

    except Exception as e:
        print(e)
        return "something is wrong"

