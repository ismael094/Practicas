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
            id_camera = row[0]
        camera.id = id_camera

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
            values (%s,%s)", (observationMode.mode, observationMode.id_camera))
            observationMode.id = self.cursor.lastrowid
            logging.info('New Observation Mode created %s' % \
            (observationMode.mode))
            return True
        except MySQLdb.Error:
            logging.error('Error while inserting a new Observation Mode named %s %s' % \
            (observationMode.mode,datetime.now().strftime("%H:%M:%S.%f")))
            return False 

class FrameDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def save(self,frame):
        sql = "insert into frame(id_camera, id_observation_mode, \
        observation_date, observation_date_microsecond, exposition_time,state,is_raw, \
        id_program, id_observation_block,path, file_name, number_extensions, number_frame, id_principal_investigator, decdeg, \
        radeg) values (%s,%s,'%s',%s,%s,'%s', %s, '%s', '%s', '%s','%s', %s, %s ,'%s', %s, %s)" % \
        (frame.id_camera, frame.id_observation_mode, \
        frame.observation_date, frame.observation_date_microsecond, \
        frame.exposition_time, frame.state, frame.is_raw, \
        frame.program,frame.blockId,frame.path,frame.file_name,\
        frame.number_extensions, frame.number_frame, \
        frame.id_principal_investigator, frame.decdeg,frame.radeg)
        try:
            self.cursor.execute(sql)
            frame.id = self.cursor.lastrowid
            logging.debug('Frame inserted')
            return True
        except MySQLdb.Error:
            logging.error('Error while inserting frame: %s' %\
            (sql))
            return False

class HeaderDefinitionDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def getId(self,headerDefinition):
        self.cursor.execute("select id from header_definition where comment = %s and \
        name= %s and data_type = %s and id_camera = %s", \
        (headerDefinition.comment,headerDefinition.name, headerDefinition.data_type, \
        headerDefinition.id_camera))
        results = self.cursor.fetchall()
        if len(results) > 0:
            for row in results:
                headerDefinition.id = row[0]
                break
        else:
            return False
    def save(self,headerDefinition):
        try:
            self.cursor.execute("insert into header_definition(comment, name, data_type, \
            visible, id_camera) values (%s,%s,%s,1,%s)", (headerDefinition.comment, \
            headerDefinition.name, headerDefinition.data_type, \
            headerDefinition.id_camera))
            logging.debug('New header definition %s' %\
            (headerDefinition.name))
            headerDefinition.id = self.cursor.lastrowid
            return True
        except MySQLdb.Error:
            logging.error('Error while creating a new header definition %s'+\
            datetime.now().strftime("%H:%M:%S.%f"))
            return False
class HeaderDefinitionSQLDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def getId(self,headerDefinition):
            return False
    def save(self,headerDefinition):
        print "IF (EXISTS(select id from header_definition where comment = '%s' and \
        name= '%s' and data_type = '%s' and id_observation_mode = '%s')) \
        THEN select id from header_definition where comment = '%s' and \
        name= '%s' and data_type = '%s' and id_observation_mode = '%s'; ELSE \
        insert into header_definition(comment, name, data_type, \
        visible, id_observation_mode) values ('%s','%s','%s',1,%s);" % \
        (headerDefinition.comment,headerDefinition.name, headerDefinition.data_type, \
        headerDefinition.id_observation_mode,headerDefinition.comment,\
        headerDefinition.name, headerDefinition.data_type, \
        headerDefinition.id_observation_mode,headerDefinition.comment,\
        headerDefinition.name, headerDefinition.data_type, \
        headerDefinition.id_observation_mode)
        headerDefinition.id = None
        return True

class HeaderDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def save(self,header,headerDefinition):
        try:  
            self.cursor.execute("insert into header(id_frame,order_keyword,extension, "+header.type+") \
            values (%s,%s,%s,%s)", (header.id_frame, header.orderKeyword, header.extension, header.value))
            header.id = self.cursor.lastrowid
            sql2 = "insert into header_definition_header values (%s, %s)" % \
            (headerDefinition.id, header.id)
            self.cursor.execute(sql2)
            logging.debug('%s = %s' %\
            (headerDefinition.name, header.value))
            return True
        except MySQLdb.Error:
            sql = "insert into header(id_frame,order_keyword,extension, "+header.type+") \
            values (%s,%s,%s,%s)" % (header.id_frame, header.orderKeyword, header.extension, header.value)
            logging.error('Error %s' %\
            (sql))
            return False
class HeaderSQLDAO(object):
    def __init__(self, cursor):
        self.cursor = cursor
    def save(self,header, headerDefinition):
        print "insert into header(id_header_definition, id_frame, \
        extension, "+header.type+") SELECT id,'%s','%s','%s' from header_definition \
        where comment = '%s' and \
        name= '%s' and data_type = '%s' and id_observation_mode = '%s';" % \
        (header.id_frame, header.extension, header.value, \
        headerDefinition.comment, headerDefinition.name, headerDefinition.data_type,\
        headerDefinition.id_observation_mode)

"""
Set
"""
def setCamera(camera,data,path):
    camera.instrument = checkKeywordObsModeCamera(data, 'INSTRUME',path)
def setObservationMode(observationMode,data,camera,path):
    observationMode.id = None
    observationMode.mode = checkKeywordObsModeCamera(data, 'OBSMODE',path)
    observationMode.id_camera = camera.id
def setFrame(frame,data,path,camera, observationMode):
    id_camera = camera  
    raw = isRaw(path)
    checkKeywordFrame(frame,data,path)
    frame.id = None
    frame.id_camera = camera
    frame.id_observation_mode = observationMode
    frame.observation_date_microsecond = 0
    frame.state = 'COMMITED'
    frame.is_raw = raw
    frame.path = orderPath(path)
    frame.file_name = getFileNamePath(path)
    frame.number_extensions = len(data)
    frame.number_frame = getNumberFrame(path)  
    if frame.blockId == '':
        logging.warning('Block ID is empty')
    return frame

def setHeaderDefinition(headerDefinitionData, headerData):
    headerDefinitionData.comment = headerData[0]
    headerDefinitionData.name = headerData[1]
    headerDefinitionData.data_type = headerData[2]
    headerDefinitionData.visible = 1
    headerDefinitionData.id_camera = headerData[3]

def setHeader(headerData, headerList):
    headerData.id_frame = headerList[1]
    headerData.extension = headerList[2]
    headerData.type = headerList[3]
    headerData.value = headerList[4]
    headerData.orderKeyword = headerList[5]

"""
Checks
"""

def isRaw(path):
    path_split = pathCut(path)
    for item in path_split:
        if item == 'raw':
            is_raw=1
            break
    else:
        is_raw=0
    return is_raw
def orderPath(path):
    path_split = pathCut(path)
    pathNoFilename = ''
    for key in path_split:
        if not key.endswith(".fits"):
            pathNoFilename += '/'+key
        else:
            pathNoFilename += '/'
    return pathNoFilename

def getFileNamePath(path):
    path_split = pathCut(path)
    path_ordered = path_split[::-1]
    return path_ordered[0]

def getDataByPath(keyword, path):
    values = {'INSTRUME' : 5 ,'OBSMODE' : 3,'DATE' : 4}
    path_split = pathCut(path)
    path_ordered = path_split[::-1]
    return path_ordered[values[keyword]]

def checkKeywordObsModeCamera(data, mode, path):
    if mode == 'INSTRUME':
        try:
            return data[0]['INSTRUME'][0]
        except KeyError:
            return getDataByPath('INSTRUME', path)
    else:
        try:
            return data[0]['OBSMODE'][0]
        except KeyError:
            return getDataByPath('OBSMODE', path)   
    logging.warning('Frame has not Keyword %s' % (mode))

def checkKeywordFrame(frame,data, path):
    keyword =['DATE','EXPTIME','GTCOBID','PI','DECDEG','RADEG']
    dataAux={}
    for key in keyword:
        try:
            dataAux[key] = data[0][key][0]
        except KeyError:
            if key == 'INSTRUME' or key == 'OBSMODE' or key == 'DATE':
                dataAux[key] = getDataByPath(key, path)
            elif key == 'DECDEG' or key == 'RADEG' or key == 'EXPTIME':
                dataAux[key] = 0
            else:
                dataAux[key] = 'None'
            logging.warning('Frame has not Keyword %s' % (key))
    frame.observation_date = dataAux['DATE']
    frame.exposition_time = dataAux['EXPTIME']
    frame.program = checkProgramKey(data)
    frame.blockId = dataAux['GTCOBID']
    frame.id_principal_investigator = dataAux['PI']
    frame.decdeg = dataAux['DECDEG']
    frame.radeg = dataAux['RADEG']


def checkProgramKey(data):
    try:
        program_key = 'GTCPRGID'
        return data[0][program_key][0]
    except KeyError:
        program_key = 'GTCPROGI'
        try:
            data[0][program_key]
            logging.warning('ProgramId key (%s) ambiguous' % (program_key))
            return data[0][program_key][0]
        except KeyError:
            logging.error('ProgramId not found')
            return 'None'
    if data[0][program_key][0] == '':
        logging.warning('ProgramId empty')

def pathCut(path): 
    path_split = path.rsplit('/')[1:]
    return path_split  


def getNumberFrame(path):
    path_split = pathCut(path)
    path_ordered = path_split[::-1]   
    frameName = path_ordered[0]
    frameNumber = frameName.rsplit('-')[::1]
    return frameNumber[0]

def getKeywordType(data):
    if type(data) == bool:
        final_type = 'LONG'
    elif type(data) == str:
        final_type = 'STRING'
    elif type(data) == float:
        final_type = 'DOUBLE'
    elif type(data) == long:
        final_type = 'LONG'
    elif type(data) == int:
        final_type = 'LONG'
    else:
        final_type = 'LONG'
    return final_type

def getInsertValue(data):
    if type(data) == bool:
        value = 'long_value'
    elif type(data) == str:
        value = 'string_value'
    elif type(data) == float:
        value = 'double_value'
    elif type(data) == long:
        value = 'long_value'
    elif type(data) == int:
        value = 'long_value'
    else:
        value = 'long_value'
    return value

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
        self.frameData = models.Frame()
        self.headerDefinition = models.HeaderDefinition()
        self.header = models.Header() 

def startScript(setModel,DAOs,args):
    route = args.route
    scan = args.scan
    default = args.default
    filepath, fileextension = os.path.splitext(route)
    if scan == True and fileextension == '': 
        start = fileScaner(setModel,DAOs,default, route)
    elif scan != True and fileextension != '':
        start = startDumpProcess(setModel,DAOs,route)

def fileScaner(setModel,DAOs,pathRoot,path1):
    a = 0
    path = pathRoot+path1
    yu = glob.glob(path)
    for dire in yu:
        for root, dirs, files in os.walk(dire):
            for fil in files:
                if fil.endswith(".fits"):
                    a+=1
                    final_root = (os.path.join(root,fil))
                    logging.debug('Frame %s open' % (final_root))
                    Open = startDumpProcess(setModel,DAOs,final_root)
                    logging.debug('Frame %s closed' % (final_root))
                    if a == 1000:
                        DAOs.db.commit()
                        a=0
    else:
        DAOs.db.commit()              

def startDumpProcess(setModel,DAOs,path):
    data = getDataFitsImages(path)
    dump = dataBasePopulator(setModel,DAOs,data, path)

def getDataFitsImages(path):
    image = fits.open(path)
    data = []
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
    return data

def dataBasePopulator(setModel,DAOs,data,path):
    logging.debug('Starting dataBasePopulatorHeader')
    dataBasePopulatorFrame(setModel,DAOs,data, path)
    for extension in range(len(data)):
        for keyword in data[extension]:
            dataBasePopulatorHeaderDefinition(setModel,DAOs,data, path,extension,keyword)
            dataBasePopulatorHeader(setModel,DAOs,data, path,extension,keyword)
def dataBasePopulatorFrame(setModel,DAOs,data,path):
    setCamera(setModel.camera, data,path)
    DAOs.cameraDAO.getId(setModel.camera)
    setObservationMode(setModel.observationMode, data, setModel.camera,path)
    if not DAOs.observationModeDAO.getId(setModel.observationMode):
        DAOs.observationModeDAO.save(setModel.observationMode)
    setFrame(setModel.frameData, data, path, setModel.camera.id, \
    setModel.observationMode.id)
    DAOs.frameDAO.save(setModel.frameData)
def dataBasePopulatorHeaderDefinition(setModel,DAOs,data,path,extension,keyword):
    value = data[extension][keyword][0]
    cameraId = setModel.frameData.id_camera
    keywordType = getKeywordType(value)
    headerDefList = [data[extension][keyword][1],keyword,\
    keywordType,cameraId]
    setHeaderDefinition(setModel.headerDefinition,headerDefList)
    if DAOs.headerDefinitionDAO.getId(setModel.headerDefinition) == False:
        DAOs.headerDefinitionDAO.save(setModel.headerDefinition)
def dataBasePopulatorHeader(setModel,DAOs,data,path,extension,keyword):
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
--The data dump has started at %s -----------\
----------------------' % \
    (datetime.now().strftime("%H:%M:%S.%f")))
    DAOs = InitDAOsAndDB()
    setModel = SetModels()
    p1 = startScript(setModel,DAOs,args)
    DAOs.db.close() 
    logging.debug('The data dump has finished at %s' % \
    (datetime.now().strftime("%H:%M:%S.%f")))