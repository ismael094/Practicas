import urllib, urllib2
import base64
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class ExtractHeader(object):
    def __init__(self):
        urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
        value={}
        self._criterias=[]
        self._operators=[]
        self.data=''
        self.lastCriteria=''
    def login(self,user,password):
        authKey = base64.b64encode(user+":"+password)
        self.headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
    def request(self):
    	self.end()
        authKey = base64.b64encode("test:test")
        headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
        urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
        request = urllib2.Request(urlBase, self.data)
        for key,value in headers.items():
            request.add_header(key,value)
            response = urllib2.urlopen(request)
        response = urllib2.urlopen(request)
        data = response.read()
        decoded = json.loads(data)
        return decoded
    def dateRequest(self, init, end):
        sentence = '{"type":"datecriteria","end":"%s","init":"%s"}' % (end,init)
        self._criterias.append(sentence)
    def programIdRequest(self, program):
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        self._criterias.append(sentence)
    def observationBlockIdRequest(self, block):
        sentence = '{"type":"observationblockidcriteria","observationBlockID":"%s"}' % (block)
        self._criterias.append(sentence)
    def instrumentRequest(self, instrument):
        sentence = '{"type":"instrumentcriteria","instrumentID":"%s"}' % (instrument)
        self._criterias.append(sentence)
    def observationModeRequest(self, obsmode):
        sentence = '{"type":"observatiomodecriteria","observationMode":"%s"}' % (obsmode)
        self._criterias.append(sentence)
    def removeRequest(self, index):
        self._criterias.pop(index)
        leng = len(self._criterias) -1 
        self.lastCriteria = ''
    def removeOperator(self, index):
        self._operators.pop(index)
    def checked(self, key):
        if self.lastCriteria == key:
            operator = self.addOperator('OR')
            self.lastCriteria = 'operator'
            return operator 
        elif self.lastCriteria == '':
            self.lastCriteria = key
        elif self.lastCriteria == 'operator':
            self.lastCriteria = key
        else:
            operator = self.addOperator('AND')
            self.lastCriteria = 'operator'
            return operator    
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
        self._operators = []
        self._criterias=[]
    def end(self):
        data='{"criterias" : ['
        obj = 0
        for item in range(len(self._criterias)):
            more = item+1
            obj += 1
            criteria = self._criterias[item]
            if more == 1:
                op = 0
                data+=self._criterias[item]
            else:
                data+=','+self._criterias[item]
            if more%2 == 0:
                try:
                    data+=','+self._operators[op]
                    op+=1
                except IndexError:
                    write = self.defaultOperator()
                    data+=','+ write
            if obj in range(4,50,4):
                division = obj/4
                for a in range(division):
                    try:
                        data+=','+self._operators[op]
                        op+=1
                    except IndexError:
                        write = self.defaultOperator()
                        data+=','+ write
            elif obj == len(self._criterias) and obj >=4:
                try:
                    data+=','+self._operators[op]
                    op+=1
                except IndexError:
                    write = self.defaultOperator()
                    data+=','+ write
        else:
            if more %2 != 0 and more > 1:
                try:
                    data+=','+self._operators[op]
                    op+=1
                except IndexError:
                    write = self.defaultOperator()
                    data+=','+ write
            data+=']}'
        self.lastCriteria = ''
        self.data = data