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
        values =  (frame.idCamera, frame.idObservationMode, \
        frame.observationDate, frame.observationDateMicrosecond, \
        frame.expositionTime, frame.state, frame.isRaw, \
        frame.program,frame.blockId,frame.path,frame.fileName,\
        frame.numberExtensions, frame.numberFrame, \
        frame.idPrincipalInvestigator, frame.decdeg,frame.radeg)
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
        headerDefinition.idCamera)
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
            headerDefinition.idCamera))
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
            "values (%s,%s,%s,'%s',%s,%s)")
        self.sentence2 = ("insert into header_definition_header values (%s, %s)")
    def save(self,header,headerDefinition):
        try: 
            if header.type == 'string_value':
                a = header.value;
                b = None
                c = None
            elif header.type == 'long_value':
                a = None
                b = header.value
                c = None
            else:
                a = None
                b = None
                c = header.value
            values = (header.idFrame, header.orderKeyword, header.extension, a,b,c)
            logging.info('DAO start')
            self.cursor.execute(self.sentence, values)
            header.id = self.cursor.lastrowid
            values2 = (headerDefinition.id, header.id)
            self.cursor.execute(self.sentence2,values2)
            logging.debug('%s = %s' % (headerDefinition.name, header.value))
            logging.info('DAO end')
            return True
        except MySQLdb.Error:
            sql = "insert into header(id_frame,order_keyword,extension, "+header.type+") \
            values (%s,%s,%s,%s)" % (header.idFrame, header.orderKeyword, header.extension,\
            header.value)
            logging.error('Error %s' % (sql))
            return False
class HeaderPDAO(object):
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
        
class HeaderSQLDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def save(self,header, headerDefinition):
        print "insert into header(id_header_definition, id_frame, \
        extension, "+header.type+") SELECT id,'%s','%s','%s' from header_definition \
        where comment = '%s' and name= '%s' and data_type = '%s' and \
        id_observation_mode = '%s';" % (header.id_frame, header.extension, header.value, \
        headerDefinition.comment, headerDefinition.name, headerDefinition.dataType,\
        headerDefinition.idObservation_mode)

"""
Set
"""
def setCamera(camera,data,checker):
    camera.instrument = checker.checkKeywordCamera(data)

def setObservationMode(observationMode,data,camera,checker):
    observationMode.id = None
    observationMode.mode = checker.checkObservationMode(data)
    observationMode.idCamera = camera.id

def setFrame(frame,data,checker,camera, observationMode):
    checker.checkKeywordFrame(frame,data)
    frame.id = None
    frame.idCamera = camera
    frame.idObservationMode = observationMode
    frame.observationDateMicrosecond = 0
    frame.state = 'COMMITED'
    frame.numberExtensions = len(data)
    return frame

def setHeaderDefinition(headerDefinitionData, headerData):
    headerDefinitionData.comment = headerData[0]
    headerDefinitionData.name = headerData[1]
    headerDefinitionData.dataType = headerData[2]
    headerDefinitionData.visible = 1
    headerDefinitionData.idCamera = headerData[3]

def setHeader(headerData, headerList):
    headerData.idFrame = headerList[1]
    headerData.extension = headerList[2]
    headerData.type = headerList[3]
    headerData.value = headerList[4]
    headerData.orderKeyword = headerList[5]

"""
Checks
"""

class Checker(object):
    def __init__(self,path):
        self.path = path
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

    def checkKeywordCamera(self,data):
        try:
            return data[0]['INSTRUME'][0]
        except KeyError:
            return self.getDataByPath('INSTRUME')
        logging.warning('Frame has not Keyword %s' % (mode))

    def getNumberFrame(self):  
        frameName = self.pathOrdered[0]
        frameNumber = frameName.rsplit('-')[::1]
        return frameNumber[0]

    def checkKeywordFrame(self,frame,data):
        keyword =['DATE','EXPTIME','GTCOBID','PI','DECDEG','RADEG']
        dataAux={}
        for key in keyword:
            try:
                dataAux[key] = data[0][key][0]
            except KeyError:
                if key == 'DATE':
                    dataAux[key] = self.getDataByPath(key)
                elif key == 'DECDEG' or key == 'RADEG' or key == 'EXPTIME':
                    dataAux[key] = 0
                else:
                    dataAux[key] = 'None'
                logging.warning('Frame has not Keyword %s' % (key))
        frame.observationDate = dataAux['DATE']
        frame.expositionTime = dataAux['EXPTIME']
        frame.program = self.checkProgramKey(data)
        frame.blockId = dataAux['GTCOBID']
        if dataAux['GTCOBID'] == '':
            logging.warning('Block ID is empty')
        frame.idPrincipalInvestigator = dataAux['PI']
        frame.decdeg = dataAux['DECDEG']
        frame.radeg = dataAux['RADEG']
        frame.isRaw = self.isRaw()
        frame.path = self.getPathWithoutFileName()
        frame.fileName = self.getFileName()
        frame.numberFrame = self.getNumberFrame() 

    def checkObservationMode(self,data):
        if self.checkKeywordCamera(data) == 'OSIRIS':
            dataAux = {}
            osirisBroadBand = ['OsirisBroasBandImage','OsirisBroadBandImages','OsirisBroadBandImaging', 'OsirisBradBandImaging', 'OsirisBroadBand']
            osirisLongSlit = ['OsirisLongSlitSpectroscop', 'OsirisLongSlitSpectgroscopy', 'LongSlitSpectroscopy', 'OsirisLongSlitSpectrosopcy']
            osirisDome = ['OsirisDomeFlats', 'OsiriDomeFlat']
            osirisSky = ['OsirisSkyFLa', 'SkyFlat']
            osirisTunable = ['TunableFilterImage','OsirisTunableFilter']
            dic = {'OsirisBroadBandImage' : osirisBroadBand, 'OsirisLongSlitSpectroscopy' : osirisLongSlit,\
            'OsirisDomeFlat' : osirisDome, 'OsirisSkyFlat' : osirisSky, 'OsirisTunableFilterImage': osirisTunable}
            
            try:
                dataAux['OBSMODE'] = data[0]['OBSMODE'][0]
            except KeyError:
                dataAux['OBSMODE'] = self.getDataByPath('OBSMODE')
            for key in dic:
                if dataAux['OBSMODE'] in dic[key]:
                    dataAux['OBSMODE'] = key
                    break
            else:
                pass
            return dataAux['OBSMODE']  

    def checkProgramKey(self,data):
        try:
            programKey = 'GTCPRGID'
            return data[0][programKey][0]
        except KeyError:
            programKey = 'GTCPROGI'
            try:
                data[0][programKey]
                logging.warning('ProgramId key (%s) ambiguous' % (programKey))
                return data[0][programKey][0]
            except KeyError:
                logging.error('ProgramId not found')
                return 'None'
        if data[0][programKey][0] == '':
            logging.warning('ProgramId empty')

def getKeywordType(data):
    types = {bool : 'LONG', str : 'STRING', float : 'DOUBLE', long : 'LONG', int : 'LONG'}
    try:
        return types[type(data)]
    except KeyError:
        return 'LONG'

def getInsertValue(data):
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
        self.headerDAO = HeaderPDAO(self.cursor)

class SetModels(object):
    def __init__(self):
        self.camera = models.Camera()
        self.observationMode = models.ObservationMode()
        self.frameData = models.Frame()
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
    checker = Checker(path)
    dump = dataBasePopulator(setModel,DAOs,data, checker)

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

def dataBasePopulator(setModel,DAOs,data,checker):
    logging.info('Starting DataBasePopulator')
    logging.info('Frame dump start')
    dataBasePopulatorFrame(setModel,DAOs,data, checker)
    logging.info('Frame dump finish')
    logging.info('Header dump start')
    for extension in range(len(data)):
        for keyword in data[extension]:
            dataBasePopulatorHeaderDefinition(setModel,DAOs,data,extension,keyword)
            dataBasePopulatorHeader(setModel,DAOs,data,extension,keyword)
    DAOs.headerDAO.save2()
    logging.info('Header dump finish')
    logging.info('DataBasePopulator end')

def dataBasePopulatorFrame(setModel,DAOs,data,checker):
    setCamera(setModel.camera, data,checker)
    DAOs.cameraDAO.getId(setModel.camera)
    setObservationMode(setModel.observationMode, data, setModel.camera,checker)
    if not DAOs.observationModeDAO.getId(setModel.observationMode):
        DAOs.observationModeDAO.save(setModel.observationMode)
    setFrame(setModel.frameData, data, checker, setModel.camera.id, \
    setModel.observationMode.id)
    DAOs.frameDAO.save(setModel.frameData)

def dataBasePopulatorHeaderDefinition(setModel,DAOs,data,extension,keyword):
    value = data[extension][keyword][0]
    cameraId = setModel.frameData.idCamera
    keywordType = getKeywordType(value)
    headerDefList = [data[extension][keyword][1],keyword,\
    keywordType,cameraId]
    setHeaderDefinition(setModel.headerDefinition,headerDefList)
    if not DAOs.headerDefinitionDAO.getId(setModel.headerDefinition):
        DAOs.headerDefinitionDAO.save(setModel.headerDefinition)

def dataBasePopulatorHeader(setModel,DAOs,data,extension,keyword):
    value = data[extension][keyword][0]
    position = data[extension][keyword][2]
    keywordInsertValue = getInsertValue(value)
    headerList = [setModel.headerDefinition.id, setModel.frameData.id, extension,\
    keywordInsertValue, value, position]
    setHeader(setModel.header,headerList)
    DAOs.headerDAO.save(setModel.header,setModel.headerDefinition)
    
if __name__ == '__main__':
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