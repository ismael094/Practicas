import urllib, urllib2
import base64
import json
import json,simplejson

ssl._create_default_https_context = ssl._create_unverified_context
class ExtractHeader(object):
    def __init__(self):
        self.urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
        value={}
        self._criterias=[]
        self._operators=[]
        self.data=''
        self.lastCriteria=''
    def login(self,user,password):
        authKey = base64.b64encode(user+":"+password)
        self.headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
    def request(self):
        request = urllib2.Request(self.urlBase, self.data)
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
    def programRequest(self, program):
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        self._criterias.append(sentence)
    def observationBlockRequest(self, block):
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

po = ExtractHeader()
po.programIdRequest('GTC1')
po.programIdRequest('GTC5')
po.addOperator('OR')
po.instrumentRequest('OSIRIS')
po.addOperator('OR')
po.end()

po.reset()
po._criterias = []
po.programIdRequest('GTC1')
po.intrumentRequest('GTC1')
po.dateRequest('2016/01/25 12:00:00','2016/01/26 12:00:00')
po.dateRequest('2016/01/25 12:00:00','2016/01/26 12:00:00')
po.observationModeRequest('AOA')
po.end()
request = urllib2.Request('https://calp-scidb1:8443/scidb/rest/frames')

exposureTime
fitsKeywords
decdeg
observationBlockId
state
isRaw
radeg
programId
camera
observationMode
observationDate
piName
path
observationDateUsec
id

modelOne= Frame()
a = 0
for item in range(len(decoded['frame'])):
    if a == 0:
        modelOne.exposition_time = []
        modelOne.decdeg = []
        modelOne.exposition_time = []
        modelOne.state = []
        modelOne.is_raw = []
        modelOne.radeg = []
        modelOne.id_program = []
        modelOne.id_camera = []
        modelOne.id_observation_mode = []
        modelOne.observation_date = []
        modelOne.id_principal_investigator = []
        modelOne.path = []
        modelOne.id = []
        a=1
    modelOne.exposition_time.append(decoded['frame'][item]['exposureTime'])
    modelOne.decdeg.append(decoded['frame'][item]['decdeg'])
    modelOne.exposition_time.append(decoded['frame'][item]['observationBlockId'])
    modelOne.state.append(decoded['frame'][item]['state'])
    modelOne.is_raw.append(decoded['frame'][item]['isRaw'])
    modelOne.radeg.append(decoded['frame'][item]['radeg'])
    modelOne.id_program.append(decoded['frame'][item]['programId'])
    modelOne.id_camera.append(decoded['frame'][item]['camera'])
    modelOne.id_observation_mode.append(decoded['frame'][item]['observationMode'])
    modelOne.observation_date.append(decoded['frame'][item]['observationDate'])
    modelOne.id_principal_investigator.append(decoded['frame'][item]['piName'])
    modelOne.path.append(decoded['frame'][item]['path'])
    modelOne.id.append(decoded['frame'][item]['id'])

data='{"criterias":[{"type":"datecriteria","end":"2014-6-27 12:00:00","init":"2014-6-1 12:00:00"},\
{"type":"programidcriteria","programID":"GTC40-14A"},\
{"type":"operatorcriteria","operator":"AND"},\
{"type":"observationblockidcriteria","observationBlockID":"0006"},\
{"type":"operatorcriteria","operator":"AND"}]}'

urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
request = urllib2.Request(urlBase, po.data)
for key,value in headers.items():
    request.add_header(key,value)
    response = urllib2.urlopen(request)

response = urllib2.urlopen(request)

data = response.read()
decoded = json.loads(data)