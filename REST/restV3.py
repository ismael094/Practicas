import urllib, urllib2
import base64
import json
import ssl
import models 
from tabulate import tabulate
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
        request = urllib2.Request(url, jsonCriterias.data)
        for key,value in self.headers.items():
            request.add_header(key,value)
            response = urllib2.urlopen(request)
        response = urllib2.urlopen(request)
        data = response.read()
        decoded = json.loads(data)
        try:
            preFrame = json.loads(data,object_hook=FrameObject)
            self.results = Result(preFrame.frame)
            print 'Request succefully'
        except AttributeError:
            print 'No image found' 
class Result(object):
    def __init__(self, frames):
        self.__frame = frames
        self.frame = frames
    def getFrames(self):
        postList = []
        for number in range(len(self.__frame)):
            pathSplit = self.__frame[number].path.rsplit('/')[1:]
            pathOrdered = pathSplit[::-1]   
            frameName = pathOrdered[0]
            preList = [self.__frame[number].id, self.__frame[number].camera.instrument,\
            self.__frame[number].observationMode.mode, self.__frame[number].observationDate, \
            self.__frame[number].programId, self.__frame[number].observationBlockId,\
            frameName, self.__frame[number].exposureTime, self.__frame[number].piName]
            postList.append(preList)
        print tabulate(postList, headers=['ID', 'Instrument', 'ObservationMode', \
        'ObservationDate','ProgramID','ObservationBlockID', 'Path', 'ExposureTime', \
        'PI'],tablefmt='orgtbl')
    def getFrameByNumber(self, number):
        pathSplit = self.__frame[number].path.rsplit('/')[1:]
        pathOrdered = pathSplit[::-1]   
        frameName = pathOrdered[0]
        postList = [[self.__frame[number].id,self.__frame[number].camera.instrument,\
        self.__frame[number].observationMode.mode, self.__frame[number].observationDate,\
        self.__frame[number].programId, self.__frame[number].observationBlockId,frameName, \
        self.__frame[number].exposureTime,self.__frame[number].piName]]
        print tabulate(postList, headers=['ID', 'Instrument', 'ObservationMode', \
        'ObservationDate','ProgramID','ObservationBlockID', 'Path', 'ExposureTime',\
        'PI'],tablefmt='orgtbl')
    def getHeaderFrame(self, number):
        postList = []
        try:
            for header in range(len(self.__frame[number].fitsKeywords)):
                if self.__frame[number].fitsKeywords[header].fitsKeywordDef.dataType == 'STRING':
                    try:
                        value = self.__frame[number].fitsKeywords[header].stringVal
                    except AttributeError:
                        value = 'NONE'
                elif self.__frame[number].fitsKeywords[header].fitsKeywordDef.dataType == 'LONG':
                    try:
                        value = self.__frame[number].fitsKeywords[header].longVal
                    except AttributeError:
                        value = 'NONE'
                elif self.__frame[number].fitsKeywords[header].fitsKeywordDef.dataType == 'DOUBLE':
                    try:
                        value = self.__frame[number].fitsKeywords[header].doubleVal
                    except AttributeError:
                        value = 'NONE'
                preList = [self.__frame[number].fitsKeywords[header].id, \
                self.__frame[number].fitsKeywords[header].fitsKeywordDef.name,\
                self.__frame[number].fitsKeywords[header].fitsKeywordDef.id, \
                self.__frame[number].fitsKeywords[header].fitsKeywordDef.dataType, \
                value]
                postList.append(preList)
        except AttributeError:
            print 'This frame has not fitsKeywords'
        print tabulate(postList, headers=['IdHeader', 'Name', 'IdHeaderDefinition', \
        'DataType','Value'],tablefmt='orgtbl')
class CriteriaBuilder(object):
    def __init__(self, criterias):
        try:
            self.__checkCriterias(criterias)
        except NameError:
            raise NameError('Error in the criterias')
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
        a = ''
        for item in range(len(criterias)):
            if criterias[item].type != 'operatorcriteria':
                stack.append(0)
            if criterias[item].type == 'operatorcriteria':  
                stack.append(1) 
        item = 0
        p = 0
        a = ''
        while item <= len(stack):
            go = item
            if '001' in a:
                for ran in range(go-1,go-4,-1):
                    stack.pop(ran)
                    go=ran
                if go < 0:
                    go = 0
                stack.insert(go,0)
                a=''
                item = 0
            else:
                try:
                    a+=str(stack[item])
                except IndexError:
                    pass
                item+=1
        if len(stack)==1 and stack[0] == 0:
            return 'WOOOOORKING'
        else:
            raise NameError('Error in criterias')

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
class PrincipalInvestigatorCriteria(object):
    def __init__(self, PI):
        self.principalInvestigator = PI
        self.type = 'principalinvestigatornamecriteria'
    def build(self):
        sentence = '{"type":"'+self.type+'","piName":"'+self.principalInvestigator+'"}'
        return sentence
class ExposureTimeCriteria(object):
    def __init__(self, startTime, operator=None,endTime=None):
        self.startTime = startTime
        self.endTime = endTime
        self.operator = operator
        self.type = 'expositiontimecriteria'
    def build(self):
        if self.endTime:
            sentence = '{"type":"'+self.type+'","exposureTime":"'+self.exposureTime+'"}'
        elif self.operator == '<':
            sentence = '{"type":"'+self.type+'","exposureTime":"'+self.exposureTime+'"}'
        elif self.operator == '>':
            sentence = '{"type":"'+self.type+'","exposureTime":"'+self.exposureTime+'"}'
        elif self.operator == '=':
            sentence = '{"type":"'+self.type+'","exposureTime":"'+self.exposureTime+'"}'
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