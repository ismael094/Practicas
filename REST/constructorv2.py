import urllib, urllib2
import base64
import json
import json,simplejson
ssl._create_default_https_context = ssl._create_unverified_context
class Date(Criterias):
    def request(self, init, end):
        self.sentence = '{"type":"datecriteria","end":"%s","init":"%s"}' % (end,init)
        self._criterias.append(final)
class programIdRequest(Criterias):
    def request(self,program):
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        self._criterias.append(final)
class observationBlock(Criterias):
    def request(self, block):
        sentence = '{"type":"observationblockidcriteria","observationBlockID":"%s"}' % (block)
        final = [sentence, 'observationblockidcriteria']
        self._criterias.append(final)
class instrument(Criterias):
    def request(self, instrument):
        sentence = '{"type":"instrumentcriteria","instrumentID":"%s"}' % (instrument)
        final = [sentence, 'instrumentcriteria']
        self._criterias.append(final)
class observationMode(Criterias):    
    def request(self, obsmode):
        sentence = '{"type":"observatiomodecriteria","observatiomodeID":"%s"}' % (obsmode)
        final = [sentence, 'observatiomodecriteria']
        self._criterias.append(final)
class Criterias(object):
    def __init__(self):
        urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
        value={}
        self._criterias=[]
        self._operators=[]
        self.lastCriteria=''
    def login(self,user,password):
        authKey = base64.b64encode(user+":"+password)
        self.headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
        
    
    def removeRequest(self, index):
        self._criterias.pop(index)
        leng = len(self._criterias) -1 
        self.lastCriteria = ''
    def addOperator(self,a):
        sentece = '{"type":"operatorcriteria","operator":"%s"}' % a
        return sentece
    def addOperatorV2(self,a):
        sentece = '{"type":"operatorcriteria","operator":"%s"}' % a
        self._operators.append(sentece)
    def reset(self):
        self.lastCriteria = ''
        self._criterias=[]
    def end(self):
        data='{"criterias" : ['
        for item in range(len(self._criterias)):
            more = item+1
            less = item -1
            criteria = self._criterias[item][1]
            if self._criterias[0][0] == self._criterias[item][0] and more == 1:
                data+=self._criterias[item][0]
            else:
                data+=','+self._criterias[item][0]
                if item%2 == 1 and item != 0:
                    data+=','+self._operators[less]
        else:
            """if self.lastCriteria != 'operator' and len(self._criterias)>1:
                write = self.addOperator('AND')
                data+=','+write"""
            leng = len(self._operators) - 1
            data+=','+self._operators[leng]
            data+=']}'
        return data

po = ExtractHeader()
po.programIdRequest('GTC1')
po.programIdRequest('GTC5')
po.end()

data='{"criterias":[{"type":"datecriteria","end":"2014-6-27 12:00:00","init":"2014-6-1 12:00:00"},\
{"type":"programidcriteria","programID":"GTC40-14A"},\
{"type":"operatorcriteria","operator":"AND"},\
{"type":"observationblockidcriteria","observationBlockID":"0006"},\
{"type":"operatorcriteria","operator":"AND"}]}'
