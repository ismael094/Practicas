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

class DateRequest(object):
    def __new__(self, init, end):
        self.init = init
        self.end = end
        sentence = '{"type":"datecriteria","end":"%s","init":"%s"}' % (end,init)
        return sentence
class ProgramRequest(object):
    def __new__(self, program):
        self.programId = program
        sentence = '{"type":"programidcriteria","programID":"%s"}' % (program)
        return sentence

class ObservationBlockRequest(object):
    def __new__(self, block):
        self.observationMode = block
        sentence = '{"type":"observationblockidcriteria","observationBlockID":"%s"}' % (block)
        return sentence

class InstrumentRequest(object):
    def __new__(self, instrument):
        self.instrument = instrument
        sentence = '{"type":"instrumentcriteria","instrumentID":"%s"}' % (instrument)
        return sentence

class ObservationModeRequest(object):
    def __new__(self, obsmode):
        self.observationMode = obsmode
        sentence = '{"type":"observatiomodecriteria","observationMode":"%s"}' % (obsmode)
        return sentence
rest = Criterias()