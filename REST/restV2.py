import urllib, urllib2
import base64
import json
import ssl
import models 
ssl._create_default_https_context = ssl._create_unverified_context

class FrameObject:
    def __init__(self, d):
        self.__dict__ = d

class Criterias(object):
    def __init__(self):
        self.urlBase='https://calp-scidb1.grantecan.net:8443/scidb/rest/frames/query?base=1&offset=50'
        value={}
        self.criterias=[]
        self._operators=[]
        self.frames = []
        self.data=''
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
        if response:
            preFrame = json.loads(data,object_hook=FrameObject)
            self.frames = preFrame.frame
        else:
            print 'No image found'
    def removeCriteria(self, index):
        self.criterias.pop(index)
    def removeOperator(self, index):
        self._operators.pop(index)   
    def defaultOperator(self):
        sentece = '{"type":"operatorcriteria","operator":"AND"}'
        return sentece
    def addOperator(self,a):
        if len(self.criterias) > 0:
            sentece = '{"type":"operatorcriteria","operator":"%s"}' % a
            self._operators.append(sentece)
        else:
            return 'No criterias'
    def reset(self):
        self.lastCriteria = ''
        self._operators = []
        self.criterias=[]
    def end(self):
        data='{"criterias" : ['
        obj = 0
        for item in range(len(self.criterias)):
            more = item+1
            obj += 1
            criteria = self.criterias[item]
            if more == 1:
                op = 0
                data+=self.criterias[item]
            else:
                data+=','+self.criterias[item]
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
            elif obj == len(self.criterias) and obj >=4:
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
        self.data = data
class Credencials(object):
    def __init__(self,user,password):
        self.user = user
        self.password = password
    def login(self):
        authKey = base64.b64encode(self.user+":"+self.password)
        headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
        return headers
class Server(object):
    def __init__(self, credencials):
        try:
            self.headers = credencials.login()
        except NameError:
            raise "No credencials"
        self.urlBase = 'https://calp-scidb1.grantecan.net:8443/scidb/rest/frames'
    def query(self, jsonCriterias, offset, limit):
        url=self.urlBase+'/query?base=%s&offset=%s' % (limit,offset)
        request = urllib2.Request(url, jsonCriterias)
        for key,value in self.headers.items():
            request.add_header(key,value)
            response = urllib2.urlopen(request)
        response = urllib2.urlopen(request)
        data = response.read()
        decoded = json.loads(data)
        try:
            preFrame = json.loads(data,object_hook=FrameObject)
            self.results = preFrame.frame
            print 'Request succefully'
        except AttributeError:
            print 'No image found' 

class CriteriaBuilder(object):
    def __new__(self, criterias):
        checkCriterias(self,criterias) 
        data = '{"criterias" : ['
        for item in range(len(criterias)):
            if item >0:
                data+=','
            data+=criterias[item].build()
        data+=']}'
        return data
    @staticmethod
    def __checkCriterias(self,criterias):
        order=[2,5,6,9,12,13,14]
        for item in range(len(Criterias)):
            if item in order:
                if criterias[item].type != 'operatorcriteria':
                    raise NameError('Error in the criterias')
            elif not item in order:
                if criterias[item].type == 'operatorcriteria':
                    raise NameError('Error in the criterias')
            else:
                p = 0
Criterias = []

class DateCriteria(object):
    def __init__(self, init, end):
        self.init = init
        self.end = end
        self.type='datecriteria'
    def build(self):
        sentence = '{"type": "'+self.type+'","end":"'+self.end+'","init":"'+self.init+'"}'
        return sentence
class ProgramCriteria(object):
    def __init__(self, program):
        self.programId = program
        self.type = 'programidcriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","programID":"'+self.programId+'"}'
        return sentence

class ObservationBlockCriteria(object):
    def __new__(self, block):
        self.observationBlock = block
        self.type = 'observationblockidcriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","observationBlockID":"'+self.observationBlock+'"}'
        return sentence

class InstrumentCriteria(object):
    def __init__(self, instrument):
        self.instrument = instrument
        self.type = 'instrumentcriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","instrumentID":"'+self.instrument+'"}'
        return sentence

class ObservationModeCriteria(object):
    def __init__(self, obsmode):
        self.observationMode = obsmode
        self.type = 'observatiomodecriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","observationMode":"'+self.observationMode+'"}'
        return sentence
class AndOperator(object):
    def __init__(self):
        self.type='operatorcriteria'
    def build(self):
        sentence = '{"type":"operatorcriteria","operator":"AND"}'
        return sentence
class OrOperator(object):
    def __init__(self):
        self.type='operatorcriteria'
    def build(self):
        sentence = '{"type":"operatorcriteria","operator":"OR"}'
        return sentence
rest = Criterias()