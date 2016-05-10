import urllib, urllib2
import base64
import json
import ssl
import copy
import models 
from tabulate import tabulate
ssl._create_default_https_context = ssl._create_unverified_context

def frameObject(d):
    p = models.Frame()
    keyList = []
    try:
        d['observationMode'] = observationModeObject(d['observationMode'])
    except KeyError:
        pass
    try:
        d['camera'] = cameraObject(d['camera'])
    except KeyError:
        pass
    try:
        for header in d['fitsKeywords']:
            keyList.append(headerObject(header))
        d['fitsKeywords'] = keyList
    except KeyError:
        pass
    p.__dict__.update(d)
    return p
def observationModeObject(d):
    p = models.ObservationMode()
    p.__dict__.update(d)
    return p

def cameraObject(d):
    p = models.Camera()
    p.__dict__.update(d)
    return p

def headerDefObject(d):
    p = models.HeaderDefinition()
    p.__dict__.update(d)
    return p

def headerObject(d):
    p = models.Header()
    d['fitsKeywordDef'] = headerDefObject(d['fitsKeywordDef'])
    p.__dict__.update(d)
    return p

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
        request = urllib2.Request(url, jsonCriterias.data)
        for key,value in self.headers.items():
            request.add_header(key,value)
            response = urllib2.urlopen(request)
        response = urllib2.urlopen(request)
        data = response.read()
        decoded = json.loads(data)
        try:
            preFrame = json.loads(data)
            self.results = Result(preFrame['frame'])
        except AttributeError:
            pass
class Result(object):
    def __init__(self, frames):
        self.__frame = frames
        self.frame = frames
    def getFrames(self):
        a = copy.deepcopy(self.__frame) 
        postList = []
        for number in range(len(a)):
            b = frameObject(a[number])
            postList.append(b)
        return postList
    def getFrameByIndex(self, number):
        a = copy.deepcopy(self.__frame) 
        return frameObject(a[number])
    def getHeaderList(self,number,headerList):
        a = copy.deepcopy(self.__frame)  
        headersList = []
        try:
            for header in a[number]['fitsKeywords']:
                if header['fitsKeywordDef']['name'] in headerList:
                    headersList.append(header)
            
        except KeyError:
            print 'This frame with index %s has not fitsKeywords' % (str(number))
        a[number]['fitsKeywords'] = headersList
        e = frameObject(a[number])

        return e
class CriteriaBuilder(object):
    def __init__(self, criterias):
        try:
            self.reCheck = self.__checkCriterias(criterias)
        except Exception:
            self.reCheck = 'False'
            raise Exception('Error in the criterias')
        data = '{"criterias" : ['
        for item in range(len(criterias)):
            if item >0:
                data+=','
            data+=criterias[item].build()
        data+=']}'
        self.data = data
    @staticmethod
    def __checkCriterias(criterias):
        stack = []
        go=0
        a = ''
        for item in range(len(criterias)):
            if criterias[item].type != 'operatorcriteria':
                stack.append(0)
                go+=1
            if criterias[item].type == 'operatorcriteria':
                if stack[go-2] == 0 and stack[go-1] == 0:
                    stack.pop(go-2)
                    go-=1
                else:
                    raise Exception('Error in the criterias')
        if len(stack)==1 and stack[0] == 0:
            return 'True'
        else:
            raise Exception('Error in criterias')

class DateCriteria(object):
    def __init__(self, init, end):
        self.init = init
        self.end = end
        self.type='datecriteria'
    def build(self):
        sentence = '{"type": "'+self.type+'","end":"'+self.end+' 12:00:00","init":"'+self.init+' 12:00:00"}'
        return sentence

class ProgramCriteria(object):
    def __init__(self, program):
        self.programId = program
        self.type = 'programidcriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","programID":"'+self.programId+'"}'
        return sentence
class ObservationBlockCriteria(object):
    def __init__(self, block):
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
class PrincipalInvestigatorCriteria(object):
    def __init__(self, PI):
        self.principalInvestigator = PI
        self.type = 'principalinvestigatornamecriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","principalInvestigator":"'+self.principalInvestigator+'"}'
        return sentence
class RegionCriteria(object):
    def __init__(self, ra, dec, rang):
        self.raDeg = ra
        self.decDeg = dec
        self.range = rang
        self.type = 'regioncriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","rigtAscention":"'+self.raDeg+'", "declination":"'+self.decDeg+'", "range":"'+str(self.range)+'"}'
        return sentence
class ExpositionTimeCriteria(object):
    def __init__(self, startTime, endTime, operator='EQ'):
        self.startTime = startTime
        self.endTime = endTime
        self.operator = operator
        self.type = 'expositiontimecriteria'
    def build(self):
        if self.operator == 'EQ':
            sentence = '{"type":"'+self.type+'","operator":"'+self.operator+'", "startTime" : "'+self.startTime+'"}'
        elif self.operator == 'LT':
            sentence = '{"type":"'+self.type+'","operator":"'+self.operator+'", "startTime" : "'+self.startTime+'"}'
        elif self.operator == 'GT':
            sentence = '{"type":"'+self.type+'", "operator":"'+self.operator+'", "startTime" : "'+self.startTime+'"}'
        elif self.operator == 'BT':
            sentence = '{"type":"'+self.type+'", "endTime" : "'+self.endTime+'", "operator":"'+self.operator+'", "startTime" : "'+self.startTime+'"}'
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