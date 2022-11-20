import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "X6AlqyH2BX-vz4QcFc3L0NzAO_HOd4hKecy6dtWLnxyt"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}




app = Flask(__name__,template_folder='template')
model = pickle.load(open("university.pkl","rb"))

@app.route("/")
def home():
    return render_template('index2.html')

@app.route("/predict", methods=["POST"])
def predict():
    gre=(request.form["gre"])
    toefl=(request.form["toefl"])
    rating=(request.form["rating"])
    sop=(request.form["sop"])
    lor=(request.form["lor"])
    cgpa=(request.form["cgpa"])
    research=request.form["research"]
    predictor=[[gre,toefl,rating,sop,lor,cgpa,research]]

##########################################################################################################################         
    #float_features = [float(x) for x in request.form.values()]
    #features = [np.array(float_features)]
    #prediction = model.predict(features)
    #prediction = prediction*0.849*100
    #return render_template("index2.html", prediction_text = "Chance of getting admission is {}%".format(prediction))

##########################################################################################################################

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']], "values": predictor}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d2e3752c-5f3b-4df3-9402-958a4c8e97dd/predictions?version=2022-11-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred == 0):
        return render_template('noChance.html')
    else:
        return render_template('chance.html')
@app.route("/back")
def back():
    return render_template('index2.html')
if __name__ == '__main__':
    app.run(debug=True)
