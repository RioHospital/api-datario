#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from urllib.request import urlopen, Request
import json

import numbers

from importlib import import_module

class RioHospitalService:
    
    '''
    __init__
    Description : initializes the properties of this service
    Precondition : -
    Postcondition : the hospital web service url has been set
    Validation : the function assigns an URL to self.hospitalWebServiceURL
    '''
    def __init__(self):
        self.hospitalWebServiceURL = "http://dadosabertos.rio.rj.gov.br/apiSaude/apresentacao/rest/index.cfm/estabelecimentos"
                    
    '''
    getHospitals
    Description : returns a Python table containing data from the hospitals dataset
    Precondition : the variable "hospitalWebServiceURL" must contain a vaild url, with a json containing the data needed.
    Postcondition : returns a Python table containing the data from the hospitals dataset.
    Validation : from the variable "hospitalWebServiceURL" the function reads a json and than proceeds to form the table to be returned.
    It does that in the two for loops contained in the function, filtering the data into the respective column
    '''    
    def getHospitals(self):
        request = Request(self.hospitalWebServiceURL)
        request.add_header('Accept', 'text/html')
        request.add_header('charset', 'utf-8')
        response = urlopen(request)
        hospitalsRaw = json.loads(str(response.read().decode('cp1252')))
        hospitals = []
        indexCounter = 0
        for columnName in hospitalsRaw['COLUMNS']:
            if columnName == "NOMEDEFANTASIA":
                nameIndex = indexCounter
            elif columnName == "LOGRADOURO":
                streetIndex = indexCounter
            elif columnName == "NUMERO":
                numberIndex = indexCounter
            elif columnName == "COMPLEMENTO":
                extraIndex = indexCounter
            elif columnName == "BAIRRO":
                neighborhoodIndex = indexCounter
            elif columnName == "CEP":
                postalCodeIndex = indexCounter
            elif columnName == "TELEFONE":
                phoneIndex = indexCounter
            elif columnName == "LATITUDE":
                latitudeIndex = indexCounter
            elif columnName == "LONGITUDE":
                longitudeIndex = indexCounter
            indexCounter = indexCounter + 1
    
        for row in hospitalsRaw['DATA']:
            if isinstance(row[numberIndex], numbers.Number):
                addressNumber = str(int(row[numberIndex]))
            else:
                addressNumber = str(row[numberIndex])
                
            if isinstance(row[extraIndex], numbers.Number):
                addressExtra = str(int(row[extraIndex]))
            else:
                addressExtra = str(row[extraIndex])
                
            if isinstance(row[phoneIndex], numbers.Number):
                phone = str(int(row[phoneIndex]))
            else:
                phone = str(row[phoneIndex])
                
            address = row[streetIndex] + " " + addressNumber + " " + addressExtra
            hospitals.append({"name": row[nameIndex], "address": address, "neighborhood": row[neighborhoodIndex], "postalCode": str(int(row[postalCodeIndex])), "phone": phone, "latitude": row[latitudeIndex], "longitude": row[longitudeIndex]})
    
        return hospitals
    
