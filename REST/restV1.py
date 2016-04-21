import urllib, urllib2
import base64
import json
import ssl
from models import frame
ssl._create_default_https_context = ssl._create_unverified_context

class Criterias(object):
    def __init__(self):
        self.urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
        value={}
        self._criterias=[]
        self._operators=[]
        self.frames = []
        self.data=''
        self.date = DateRequest(self)
        self.program = ProgramRequest(self)
        self.observationMode = ObservationModeRequest(self)
        self.observationBlock = ObservationBlockRequest(self)
        self.instrument = InstrumentRequest(self)
    def login(self,user,password):
        authKey = base64.b64encode(user+":"+password)
        self.headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
    def request(self):
        self.end()
        self.login('test', 'test')
        request = urllib2.Request(self.urlBase, self.data)
        for key,value in self.headers.items():
            request.add_header(key,value)
            response = urllib2.urlopen(request)
        response = urllib2.urlopen(request)
        data = response.read()
        decoded = json.loads(data)
        self.setFrame(decoded)
    def setFrame(self, data):
        for image in range(len(data['frame'])):
            frame = models.Frame()
            frame.exposition_time = data['frame'][image]['exposureTime']
            frame.decdeg = data['frame'][image]['decdeg']
            frame.exposition_time = data['frame'][image]['observationBlockId']
            frame.state = data['frame'][image]['state']
            frame.is_raw = data['frame'][image]['isRaw']
            frame.radeg = data['frame'][image]['radeg']
            frame.id_program = data['frame'][image]['programId']
            frame.id_camera = data['frame'][image]['camera']
            frame.id_observation_mode = data['frame'][image]['observationMode']
            frame.observation_date = data['frame'][image]['observationDate']
            frame.id_principal_investigator = data['frame'][image]['piName']
            frame.path = data['frame'][image]['path']
            frame.id =data['frame'][image]['id']
            frame.header = []
            for item in range(len(data['frame'][image]['fitsKeywords'])):
                headerData = models.Header()
                for key in data['frame'][image]['fitsKeywords'][item]:
                    if key == 'fitsKeywordDef' and key != 'id':
                        headerData.definition = models.HeaderDefinition()
                        headerData.definition.id = data['frame'][image]['fitsKeywords'][item]['fitsKeywordDef']['id']
                        headerData.definition.comment = data['frame'][image]['fitsKeywords'][item]['fitsKeywordDef']['comment']
                        headerData.definition.name = data['frame'][image]['fitsKeywords'][item]['fitsKeywordDef']['name']
                        headerData.definition.data_type = data['frame'][image]['fitsKeywords'][item]['fitsKeywordDef']['dataType']
                        headerData.definition.visible = data['frame'][image]['fitsKeywords'][item]['fitsKeywordDef']['visible']
                        headerData.definition.id_observation_mode = data['frame'][image]['fitsKeywords'][item]['fitsKeywordDef']['obsMode']
                    elif key == 'id':
                        headerData.id = data['frame'][image]['fitsKeywords'][item]['id']
                        headerData.id_header_definition = data['frame'][image]['fitsKeywords'][item]['fitsKeywordDef']['id']
                        headerData.id_frame = frame.id
                    else:
                        if key == 'longVal':
                            headerData.long_value = data['frame'][image]['fitsKeywords'][item][key]
                        elif key == 'doubleVal':
                            headerData.double_value = data['frame'][image]['fitsKeywords'][item][key]
                        else:
                            headerData.string_value = data['frame'][image]['fitsKeywords'][item][key]
                frame.header.append(headerData)
            self.frames.append(frame)
    def removeCriteria(self, index):
        self._criterias.pop(index)
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
            return 'No criterias'
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

class DateRequest(object):
    def __init__(self, criterias):
        self.init = None
        self.criteria = criterias
        self.end = None
    def set(self, init, end):
        self.init = init
        self.end = end
        sentence = '{"type":"datecriteria","end":"%s","init":"%s"}' % (end,init)
        self.criteria._criterias.append(sentence)

class ProgramRequest(object):
    def __init__(self, criterias):
        self.programId = None
        self.criteria = criterias
    def set(self, program):
        self.programId = program
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        self.criteria._criterias.append(sentence)

class ObservationBlockRequest(object):
    def __init__(self, criterias):
        self.observationMode = None
        self.criteria = criterias
    def set(self, block):
        self.observationMode = block
        sentence = '{"type":"observationblockidcriteria","observationBlockID":"%s"}' % (block)
        self.criteria._criterias.append(sentence)

class InstrumentRequest(object):
    def __init__(self, criterias):
        self.instrument = None
        self.criteria = criterias
    def set(self, instrument):
        self.instrument = instrument
        sentence = '{"type":"instrumentcriteria","instrumentID":"%s"}' % (instrument)
        self.criteria._criterias.append(sentence)

class ObservationModeRequest(object):
    def __init__(self, criterias):
        self.observationMode = None
        self.criteria = criterias
    def set(self, obsmode):
        self.observationMode = obsmode
        sentence = '{"type":"observatiomodecriteria","observationMode":"%s"}' % (obsmode)
        self.criteria._criterias.append(sentence)
