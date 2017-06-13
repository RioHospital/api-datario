#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response

from functools import wraps

from riohospital import RioHospitalService

import json
import os

app = Flask(__name__)

rioHospitalService = RioHospitalService()

'''
return_json
Description: Converts a Python table to json format
Precondition : f is a valid table
Postcondition : returns f in json format
Validation : the function json.dumps and Response does the necessary transformations to f
'''
def return_json(f):
    @wraps(f)
    def inner(*a, **k):
        json_response = json.dumps((f(*a, **k)),ensure_ascii = False)
        response = Response(json_response,content_type="application/json; charset=utf-8" )
        return response
    return inner

'''
getHospitals
Description : returns a Python table containing data from the hospitals dataset
Precondition : the variable "rioHospitalService" must have been properly initialized
Postcondition : returns a table with the necessary data from the hospitals dataset
Validation : calls the function getHospitals which is validated
'''
@app.route('/hospitals')
@return_json 
def getHospitals():
    return rioHospitalService.getHospitals()

'''
getHealthInsurancePlans
Description : returns a Python table with the needed data from the health insurance plans.
Precondition : the variable "rioHospitalService" must have been properly initialized
Postcondition : returns a table with the necessary data from the health insurance plans dataset
Validation : calls the function getHealthInsurancePlans which is validated 
'''
@app.route('/healthInsurancePlans')
@return_json 
def getHealthInsurancePlans():
    return rioHospitalService.getHealthInsurancePlans()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
