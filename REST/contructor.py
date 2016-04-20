import urllib, urllib2
import base64
import json
import json,simplejson
ssl._create_default_https_context = ssl._create_unverified_context
class ExtractHeader(object):
    def __init__(self):
        urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
        value={}
        self._criterias=[]
        self.lastCriteria=''
    def login(self,user,password):
        authKey = base64.b64encode(user+":"+password)
        self.headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
    def dateRequest(self, init, end):
        sentence = '{"type":"datecriteria","end":"%s","init":"%s"}' % (end,init)
        final = [sentence, 'datecriteria']
        self._criterias.append(final)
    def programIdRequest(self, program):
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        final = [sentence, 'programidcriteria']
        self._criterias.append(final)
    def observationBlockIdRequest(self, block):
        sentence = '{"type":"observationblockidcriteria","observationBlockID":"%s"}' % (block)
        final = [sentence, 'observationblockidcriteria']
        self._criterias.append(final)
    def intrumentRequest(self, instrument):
        sentence = '{"type":"instrumentcriteria","instrumentID":"%s"}' % (instrument)
        final = [sentence, 'instrumentcriteria']
        self._criterias.append(final)
    def observationModeRequest(self, obsmode):
        sentence = '{"type":"observatiomodecriteria","observatiomodeID":"%s"}' % (obsmode)
        final = [sentence, 'observatiomodecriteria']
        self._criterias.append(final)
    def removeRequest(self, index):
        self._criterias.pop(index)
        leng = len(self._criterias) -1 
        self.lastCriteria = ''
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
    def addOperator(self,a):
        sentece = '{"type":"operatorcriteria","operator":"%s"}' % a
        return sentece
    def reset(self):
        self.lastCriteria = ''
        self._criterias=[]
    def end(self,ele):
        data='{"criterias" : ['
        for item in range(len(self._criterias)):
            more = item+1
            criteria = self._criterias[item][1]
            if self._criterias[0][0] == self._criterias[item][0] and more == 1:
                data+=self._criterias[item][0]
                self.checked(self._criterias[item][1])
            else:
                data+=','+self._criterias[item][0]
                if more%2 == 0:
                    write = self.checked(criteria)
                    data+=','+write
                else:
                    write = self.checked(criteria)
                for num in range(4,24,4):
                    if more == num:
                        write = self.addOperator(ele)
                        data+=','+write
        else:
            write = self.addOperator(ele)
            data+=','+write
            data+=']}'
        self.lastCriteria = ''
        return data

po = ExtractHeader()
po.programIdRequest('GTC1')
po.programIdRequest('GTC5')
po.end()

po.reset()
po._criterias = []
po.programIdRequest('GTC1')
po.intrumentRequest('GTC1')
po.dateRequest('2016/01/25 12:00:00','2016/01/26 12:00:00')
po.dateRequest('2016/01/25 12:00:00','2016/01/26 12:00:00')
po.observationModeRequest('AOA')
po.end()


data='{"criterias":[{"type":"datecriteria","end":"2014-6-27 12:00:00","init":"2014-6-1 12:00:00"},\
{"type":"programidcriteria","programID":"GTC40-14A"},\
{"type":"operatorcriteria","operator":"AND"},\
{"type":"observationblockidcriteria","observationBlockID":"0006"},\
{"type":"operatorcriteria","operator":"AND"}]}'
