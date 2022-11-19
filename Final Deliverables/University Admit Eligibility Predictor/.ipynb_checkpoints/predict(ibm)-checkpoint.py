# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 21:11:24 2022

@author: Prathap
"""

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "X6AlqyH2BX-vz4QcFc3L0NzAO_HOd4hKecy6dtWLnxyt"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']], "values": features}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d2e3752c-5f3b-4df3-9402-958a4c8e97dd/predictions?version=2022-11-10', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions = response_scoring.json()
print(predictions)
pred = predictions['predictions'][0]['values'][0][0]

if(pred != 0):
	print("Chances to eligibility")
else:
	print("No chances for eligiblity")
