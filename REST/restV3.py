import urllib, urllib2
import base64
import json
import ssl
import models 
ssl._create_default_https_context = ssl._create_unverified_context

class FrameObject:
    def __init__(self, d):
        self.__dict__ = d

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
class Result(object):
    def __init__(self, frames):
        self.__frame = frames
    def getFrames(self):
        print self.__frame
    def getFrameByNumber(self, number):
        print self.__frame[number]

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