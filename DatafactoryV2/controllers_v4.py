from astropy.io import fits
from datetime import datetime
import models
import argparse
import os
import time
import logging
import sys
import MySQLdb
import glob
"""
DAO
"""
class CameraDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def getId(self,camera):
        self.cursor.execute("select id from camera where instrument = '"+\
        camera.instrument+"'")
        results = self.cursor.fetchall()
        for row in results:
            idCamera = row[0]
        camera.id = idCamera

class ObservationModeDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def getId(self,observationMode):
        self.cursor.execute("select id, id_camera from observation_mode \
        where mode = '"+observationMode.mode+"'")
        results = self.cursor.fetchall()
        for row1 in results:
            observationMode.id = row1[0]
            return True
            break
        else:
            self.id = False
    def save(self,observationMode):
        try:
            self.cursor.execute("insert into observation_mode(mode,id_camera) \
            values (%s,%s)", (observationMode.mode, observationMode.idCamera))
            observationMode.id = self.cursor.lastrowid
            logging.info('New Observation Mode created %s' % \
            (observationMode.mode))
            return True
        except MySQLdb.Error:
            logging.error('Error while inserting a new Observation Mode named %s ' % \
            (observationMode.mode))
            return False 

class FrameDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
        self.sentence = ("insert into frame(id_camera, id_observation_mode, \
        observation_date, observation_date_microsecond, exposition_time,state,is_raw, \
        id_program, id_observation_block,path, file_name, number_extensions, number_frame, id_principal_investigator, decdeg, \
        radeg) values (%s,%s,%s,%s,%s,%s, %s, %s, %s, %s,%s, %s, %s ,%s, %s, %s)")
    
    def save(self,frame):
        values =  (frame.camera.id, frame.observationMode.id, \
        frame.observationDate, frame.observationDateMicrosecond, \
        frame.exposureTime, frame.state, frame.isRaw, \
        frame.programId,frame.observationBlockId,frame.path,frame.fileName,\
        frame.numberExtensions, frame.numberFrame, \
        frame.piName, frame.decdeg,frame.radeg)
        try:
            self.cursor.execute(self.sentence, values)
            frame.id = self.cursor.lastrowid
            logging.debug('Frame inserted')
            return True
        except MySQLdb.Error:
            logging.error('Error while inserting frame: %s' %\
            (self.sentence % values))
            return False

class HeaderDefinitionDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
        self.sentence = ("select id from header_definition where comment = %s and \
        name= %s and data_type = %s and id_camera = %s")
    def getId(self,headerDefinition):
        values = (headerDefinition.comment,headerDefinition.name, headerDefinition.dataType, \
        headerDefinition.camera.id)
        self.cursor.execute(self.sentence, values)
        results = self.cursor.fetchall()

        if len(results) > 0:
            for row in results:
                headerDefinition.id = row[0]
                return True
                break
        else:
            return False
    def save(self,headerDefinition):
        try:
            self.cursor.execute("insert into header_definition(comment, name, data_type, \
            visible, id_camera) values (%s,%s,%s,1,%s)", (headerDefinition.comment, \
            headerDefinition.name, headerDefinition.dataType, \
            headerDefinition.camera.id))
            logging.debug('New header definition %s' %\
            (headerDefinition.name))
            headerDefinition.id = self.cursor.lastrowid
            return True
        except MySQLdb.Error:
            logging.error('Error while creating a new header definition %s'+\
            datetime.now().strftime("%H:%M:%S.%f"))
            return False

class HeaderDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
        self.sentence = ("insert into header "
            "(id_frame,order_keyword,extension, string_value, long_value, double_value) "
            "values (%s,%s,%s,%s,%s,%s)")
        self.sentence2 = ("insert into header_definition_header(id_header_definition,id_header)\
        values (%s, %s)")
        self.sentence2Data = []
    def save(self,header,headerDefinition):
        try: 
            string = None
            longVal = None
            double = None
            if header.type == 'string_value':
                string = header.value
            elif header.type == 'long_value':
                longVal = header.value
            else:
                double = header.value
            values = (header.idFrame, header.orderKeyword, header.extension, string,longVal,double)
            self.cursor.execute(self.sentence, values)
            header.id = self.cursor.lastrowid
            self.sentence2Data.append((int(headerDefinition.id), int(header.id)))   
            logging.debug('%s = %s' % (headerDefinition.name, header.value))
            return True
        except MySQLdb.Error:
            sql = "insert into header(id_frame,order_keyword,extension, string_value,long_value,\
            double_value) values (%s,%s,%s,'%s',%s,%s)" % (header.idFrame, header.orderKeyword, \
            header.extension, string,longVal,double)
            logging.error('Error %s' % (sql))
            return False
    def save2(self):
        self.cursor.executemany(self.sentence2,self.sentence2Data)
        self.sentence2Data = []

"""
Set
"""
class SetDataIntoModels(object):
    def __init__(self,data, models,checker):
        self.data = data
        self.checker = checker
        self.models = models

    def setCamera(self):
        self.models.camera.instrument = self.checker.checkKeywordCamera()

    def setObservationMode(self):
        self.models.observationMode.id = None
        self.models.observationMode.mode = self.checker.checkObservationMode()
        self.models.observationMode.idCamera = self.models.camera.id

    def setFrame(self):
        self.checker.checkKeywordFrame(self.models.frame)
        self.models.frame.id = None
        self.models.frame.camera = self.models.camera
        self.models.frame.observationMode = self.models.observationMode
        self.models.frame.observationDateMicrosecond = 0
        self.models.frame.state = 'COMMITED'
        self.models.frame.numberExtensions = len(self.data)

    def setHeaderDefinition(self, headerData):
        self.models.headerDefinition.comment = headerData[0]
        self.models.headerDefinition.name = headerData[1]
        self.models.headerDefinition.dataType = headerData[2]
        self.models.headerDefinition.visible = False
        self.models.headerDefinition.camera = self.models.camera

    def setHeader(self, headerList):
        self.models.header.idFrame = self.models.frame.id
        self.models.header.extension = headerList[0]
        self.models.header.type = headerList[1]
        self.models.header.value = headerList[2]
        self.models.header.orderKeyword = headerList[3]

"""
Checks
"""

class Checker(object):
    def __init__(self,path,data):
        self.path = path
        self.data = data
        self.pathSplit = path.rsplit('/')[1:]
        self.pathOrdered = self.pathSplit[::-1]
    def isRaw(self):
        for item in self.pathSplit:
            if item == 'raw':
                isRaw=1
                break
        else:
            isRaw=0
        return isRaw

    def getPathWithoutFileName(self):
        pathSplit = self.pathSplit
        pathSplit.pop()
        pathNoFilename = '/'
        pathNoFilename+="/".join(pathSplit)
        return pathNoFilename

    def getFileName(self):
        return self.pathOrdered[0]

    def getDataByPath(self,keyword):
        values = {'INSTRUME' : 5 ,'OBSMODE' : 3,'DATE' : 4}
        return self.pathOrdered[values[keyword]]

    def checkKeywordCamera(self):
        try:
            return self.data[0]['INSTRUME'][0]
        except KeyError:
            return self.getDataByPath('INSTRUME')
        logging.warning('Frame has not Keyword %s' % (mode))

    def getNumberFrame(self):  
        frameName = self.pathOrdered[0]
        frameNumber = frameName.rsplit('-')[::1]
        return frameNumber[0]

    def checkKeywordFrame(self,frame):
        keyword =['DATE','EXPTIME','GTCOBID','PI','DECDEG','RADEG']
        dataAux={}
        for key in keyword:
            try:
                dataAux[key] = self.data[0][key][0]
            except KeyError:
                if key == 'DATE':
                    dataAux[key] = self.getDataByPath(key)
                elif key == 'DECDEG' or key == 'RADEG' or key == 'EXPTIME':
                    dataAux[key] = 0
                else:
                    dataAux[key] = 'None'
                logging.warning('Frame has not Keyword %s' % (key))
        frame.observationDate = dataAux['DATE']
        frame.exposureTime = dataAux['EXPTIME']
        frame.programId = self.checkProgramKey()
        frame.observationBlockId = dataAux['GTCOBID']
        if dataAux['GTCOBID'] == '':
            logging.warning('Block ID is empty')
        frame.piName = dataAux['PI']
        frame.decdeg = dataAux['DECDEG']
        frame.radeg = dataAux['RADEG']
        frame.isRaw = self.isRaw()
        frame.path = self.getPathWithoutFileName()
        frame.fileName = self.getFileName()
        frame.numberFrame = self.getNumberFrame() 

    def checkObservationMode(self):
        if self.checkKeywordCamera() == 'OSIRIS':
            dataAux = {}
            osirisBroadBand = ['OsirisBroasBandImage','OsirisBroadBandImages','OsirisBroadBandImaging', 'OsirisBradBandImaging', 'OsirisBroadBand']
            osirisLongSlit = ['OsirisLongSlitSpectroscop', 'OsirisLongSlitSpectgroscopy', 'LongSlitSpectroscopy', 'OsirisLongSlitSpectrosopcy']
            osirisDome = ['OsirisDomeFlats', 'OsiriDomeFlat']
            osirisSky = ['OsirisSkyFLa', 'SkyFlat']
            osirisTunable = ['TunableFilterImage','OsirisTunableFilter']
            dic = {'OsirisBroadBandImage' : osirisBroadBand, 'OsirisLongSlitSpectroscopy' : osirisLongSlit,\
            'OsirisDomeFlat' : osirisDome, 'OsirisSkyFlat' : osirisSky, 'OsirisTunableFilterImage': osirisTunable}
            
            try:
                dataAux['OBSMODE'] = self.data[0]['OBSMODE'][0]
            except KeyError:
                dataAux['OBSMODE'] = self.getDataByPath('OBSMODE')
            for key in dic:
                if dataAux['OBSMODE'] in dic[key]:
                    dataAux['OBSMODE'] = key
                    break
            else:
                pass
            return dataAux['OBSMODE']  

    def checkProgramKey(self):
        try:
            programKey = 'GTCPRGID'
            return self.data[0][programKey][0]
        except KeyError:
            programKey = 'GTCPROGI'
            try:
                self.data[0][programKey]
                logging.warning('ProgramId key (%s) ambiguous' % (programKey))
                return self.data[0][programKey][0]
            except KeyError:
                logging.error('ProgramId not found')
                return 'None'
        if self.data[0][programKey][0] == '':
            logging.warning('ProgramId empty')

    def getKeywordType(self,data):
        types = {bool : 'LONG', str : 'STRING', float : 'DOUBLE', long : 'LONG', int : 'LONG'}
        try:
            return types[type(data)]
        except KeyError:
            return 'LONG'

    def getInsertValue(self,data):
        types = {bool : 'long_value', str : 'string_value', float : 'double_value', long : 'long_value', int : 'long_value'}
        try:
            return types[type(data)]
        except KeyError:
            return 'LONG'


"""
Controllers
"""
class InitDAOsAndDB(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "ismael", "123456", "datafactoryv2")
        self.cursor = self.db.cursor()
        self.frameDAO = FrameDAO(self.cursor)
        self.cameraDAO = CameraDAO(self.cursor)
        self.observationModeDAO = ObservationModeDAO(self.cursor)
        self.headerDefinitionDAO = HeaderDefinitionDAO(self.cursor)
        self.headerDAO = HeaderDAO(self.cursor)

class SetModels(object):
    def __init__(self):
        self.camera = models.Camera()
        self.observationMode = models.ObservationMode()
        self.frame = models.Frame()
        self.headerDefinition = models.HeaderDefinition()
        self.header = models.Header() 

def startScript(args):
    DAOs = InitDAOsAndDB()
    setModel = SetModels()
    route = args.route
    scan = args.scan
    default = args.default
    filepath, fileextension = os.path.splitext(route)
    if scan == True and fileextension == '': 
        start = fileScaner(setModel,DAOs,default, route)
    elif scan != True and fileextension != '':
        start = startDumpProcess(setModel,DAOs,route)
    DAOs.db.close()

def fileScaner(setModel,DAOs,pathRoot,path1):
    a = 0
    path = pathRoot+path1
    yu = glob.glob(path)
    for dire in yu:
        for root, dirs, files in os.walk(dire):
            for fil in files:
                if fil.endswith(".fits"):
                    logging.info('filescaner_begin')
                    a+=1
                    final_root = (os.path.join(root,fil))
                    logging.info('Frame %s open' % (final_root))
                    Open = startDumpProcess(setModel,DAOs,final_root)
                    logging.info('Frame %s closed' % (final_root))
                    if a == 100:
                        DAOs.db.commit()
                        a=0
                    logging.info('filescaner_end')
    else:
        DAOs.db.commit()              

def startDumpProcess(setModel,DAOs,path):
    data = getDataFitsImages(path)
    checker = Checker(path,data)
    dump = DataBasePopulator(setModel,DAOs,data, checker)
    dump.startPopulator()

def getDataFitsImages(path):
    image = fits.open(path)
    data = []
    logging.info('Starting getDataFitsImages')
    for extension in range(len(image)):
        datas = {}
        position = 0
        for keyword in image[extension].header:
            if keyword != 'COMMENT':
                position+=1
                datas[keyword] = [image[extension].header[keyword],\
                image[extension].header.comments[keyword], position]
        data.append(datas)
    image.close()
    logging.info('getDataFitsImages done')
    return data
class DataBasePopulator(object):
    def __init__(self, models, DAOs, data, checker):
        self.models = models
        self.DAOs = DAOs
        self.data = data
        self.checker = checker
        self.setter = SetDataIntoModels(self.data,self.models,self.checker)
    def startPopulator(self):
        logging.info('Starting DataBasePopulator')
        logging.info('Frame dump start')
        self.framePopulator()
        logging.info('Frame dump finish')
        logging.info('Header dump start')
        for extension in range(len(self.data)):
            for keyword in self.data[extension]:
                self.headerDefinitionPopulator(extension,keyword)
                self.headerPopulator(extension,keyword)
        self.DAOs.headerDAO.save2()
        logging.info('Header dump finish')
        logging.info('DataBasePopulator end')

    def framePopulator(self):
        self.setter.setCamera()
        self.DAOs.cameraDAO.getId(self.models.camera)
        self.setter.setObservationMode()
        if not self.DAOs.observationModeDAO.getId(self.models.observationMode):
            self.DAOs.observationModeDAO.save(self.models.observationMode)
        self.setter.setFrame()
        self.DAOs.frameDAO.save(self.models.frame)

    def headerDefinitionPopulator(self,extension,keyword):
        value = self.data[extension][keyword][0]
        keywordType = self.checker.getKeywordType(value)
        headerDefList = [self.data[extension][keyword][1],keyword,\
        keywordType]
        self.setter.setHeaderDefinition(headerDefList)
        if not self.DAOs.headerDefinitionDAO.getId(self.models.headerDefinition):
            self.DAOs.headerDefinitionDAO.save(self.models.headerDefinition)

    def headerPopulator(self, extension,keyword):
        value = self.data[extension][keyword][0]
        position = self.data[extension][keyword][2]
        keywordInsertValue = self.checker.getInsertValue(value)
        headerList = [extension, keywordInsertValue, value, position]
        self.setter.setHeader(headerList)
        self.DAOs.headerDAO.save(self.models.header,self.models.headerDefinition)
    
if __name__ == '__main__':
    

    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'

    logging.basicConfig(filename='logs.log',level=logging.DEBUG, format=FORMAT)
    now = time.strftime("%c")
    parser = argparse.ArgumentParser(description="Do you wish to scan?")
    parser.add_argument("-r", dest='route', action='store',help='Route\
    of the instrument and the date that you want to dump')
    parser.add_argument("-s", dest='scan', action='store',\
    help='Scan files in a directory', default=True)
    parser.add_argument("-d", dest='default', action='store',\
    help='Use default route', default='/scidb/framedb/')
    args = parser.parse_args()
    logging.debug('--------------------------------------\
--The data dump has started-----------\
----------------------' )
    
    p1 = startScript(args)
    logging.debug('The data dump has finished')