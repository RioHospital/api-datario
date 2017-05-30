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
    Pre-Condição :  
    Pós-Condição : 
    '''
    def __init__(self):
        self.hospitalWebServiceURL = "http://dadosabertos.rio.rj.gov.br/apiSaude/apresentacao/rest/index.cfm/estabelecimentos"
        self.healthInsurancePlans = []
        pluginPath = "healthInsurancePlans"
        
        for filename in os.listdir(pluginPath):
            module_name, ext = os.path.splitext(filename)
            
            if ext == '.py':
                try:
                    module = import_module(pluginPath + "." + module_name)
                    
                    for classname in dir(module):
                        if classname.startswith("Plan_"):
                            self.healthInsurancePlans.append(getattr(module, classname)())
                            
                except Exception as e:
                    sys.stderr.write('unable to load module: %s: %s\n' % (filename, e))
                    continue
                    
    '''
    Pre-Condição : a variavel "hospitalWebServiceURL" seja uma url valida, contendo json desejado.
    Pós-Condição : retorna uma array contendo os dados desejados dos hospitais contidos na url
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
     
    '''
    Pre-Condição : a variavel "healthInsurancePlans" deve conter todos os planos de saude necessarios  
    Pós-Condição : retornar uma array contendo id e nome dos planos de saude
    '''    
    def getHealthInsurancePlans(self):
        jsonData = []
        
        for healthInsurancePlan in self.healthInsurancePlans:
            jsonData.append({"id": healthInsurancePlan.getId(), "name": healthInsurancePlan.getName()})
            
        return jsonData
