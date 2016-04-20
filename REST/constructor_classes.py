import urllib, urllib2
import base64
import json
import json,simplejson
ssl._create_default_https_context = ssl._create_unverified_context

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
    def dateRequest(self, init, end):
        sentence = '{"type":"datecriteria","end":"%s","init":"%s"}' % (end,init)
        self._criterias.append(sentence)
    def programIdRequest(self, program):
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        self._criterias.append(sentence)
    def observationBlockIdRequest(self, block):
        sentence = '{"type":"observationblockidcriteria","observationBlockID":"%s"}' % (block)
        self._criterias.append(sentence)
    def intrumentRequest(self, instrument):
        sentence = '{"type":"instrumentcriteria","instrumentID":"%s"}' % (instrument)
        self._criterias.append(sentence)
    def observationModeRequest(self, obsmode):
        sentence = '{"type":"observatiomodeidcriteria","observationMode":"%s"}' % (obsmode)
        self._criterias.append(sentence)
    def removeRequest(self, index):
        self._criterias.pop(index)
        leng = len(self._criterias) -1 
        self.lastCriteria = ''
    def defaultOperator(self):
        sentece = '{"type":"operatorcriteria","operator":"AND"}'
        return sentece
    def addOperator(self,a):
        if len(self._criterias) > 0:
            sentece = '{"type":"operatorcriteria","operator":"%s"}' % a
            self._operators.append(sentece)
        else:
            return 'Fail'
    def reset(self):
        self.lastCriteria = ''
        self._criterias=[]
    def end(self):
        data='{"criterias" : ['
        for item in range(len(self._criterias)):
            more = item+1
            if more == 1:
                op = 0
                data+=self._criterias[item][0]
            else:
                data+=','+self._criterias[item][0]
            if more%2 == 0:
                try:
                    data+=','+self._operators[op]
                    op+=1
                except IndexError:
                    write = self.defaultOperator()
                    data+=','+ write
        else:
            if more %2 != 0:
                try:
                    data+=','+self._operators[op]
                    op+=1
                except IndexError:
                    write = self.defaultOperator()
                    data+=','+ write
            data+=']}'
        return data
class Date(Criterias):
    def __init__(self):
        self.init= None
        self.end=None
    def request(self, init, end):
        self.init= init
        self.end=end
        self.sentence = '{"type":"datecriteria","end":"%s","init":"%s"}' % (end,init)
        self._criterias.append(final)

class ProgramIdRequest(Criterias):
    def __init__(self):
        self.program=None
    def request(self,program):
        self.program=program
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        self._criterias.append(final)

class ObservationBlock(Criterias):
    def __init__(self):
        self.observationBlock=None
    def request(self, block):
        self.observationBlock=block
        sentence = '{"type":"observationblockidcriteria","observationBlockID":"%s"}' % (block)
        self._criterias.append(final)

class Instrument(Criterias):
    def __init__(self):
        self.instrument=None
    def request(self, instrument):
        self.instrument=instrument
        sentence = '{"type":"instrumentcriteria","instrumentID":"%s"}' % (instrument)
        self._criterias.append(final)

class ObservationMode(Criterias):  
    def __init__(self):
        self.observationMode=None
    def request(self, obsmode):
        self.observationMode=obsmode
        sentence = '{"type":"observatiomodecriteria","observatiomodeID":"%s"}' % (obsmode)
        self._criterias.append(final)

po = ExtractHeader()
po.programIdRequest('GTC1')
po.programIdRequest('GTC5')
po.end()

data='{"criterias":[{"type":"datecriteria","end":"2014-6-27 12:00:00","init":"2014-6-1 12:00:00"},\
{"type":"programidcriteria","programID":"GTC40-14A"},\
{"type":"operatorcriteria","operator":"AND"},\
{"type":"observationblockidcriteria","observationBlockID":"0006"},\
{"type":"operatorcriteria","operator":"AND"}]}'

urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
request = urllib2.Request(urlBase, data)
for key,value in headers.items():
    request.add_header(key,value)
    response = urllib2.urlopen(request)

response = urllib2.urlopen(request)

data = response.read()
decoded = json.loads(data)