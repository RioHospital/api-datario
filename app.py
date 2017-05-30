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
Pre-Condição :  
Pós-Condição : 
'''
def return_json(f):
    @wraps(f)
    def inner(*a, **k):
        json_response = json.dumps((f(*a, **k)),ensure_ascii = False)
        response = Response(json_response,content_type="application/json; charset=utf-8" )
        return response
    return inner

'''
Pre-Condição : a variavel "rioHospitalService" deve estar propriamente inicializada
Pós-Condição : retorna a array contendo os dados desejados dos hospitais
'''
@app.route('/hospitals')
@return_json 
def getHospitals():
    return rioHospitalService.getHospitals()

'''
Pre-Condição : a variavel "rioHospitalService" deve estar propriamente inicializada
Pós-Condição : retorna a array contendo os dados desejados dos planos de saude
'''
@app.route('/healthInsurancePlans')
@return_json 
def getHealthInsurancePlans():
    return rioHospitalService.getHealthInsurancePlans()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
