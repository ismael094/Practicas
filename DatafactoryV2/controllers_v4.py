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
            logging.info('A new Observation Mode named %s has been created  %s' % \
            (observationMode.mode,datetime.now().strftime("%H:%M:%S.%f")))
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
        id_program, id_observation_block,path, number_extensions, number_frame, id_principal_investigator, decdeg, \
        radeg) values (%s,%s,'%s',%s,%s,'%s', %s, '%s', '%s', '%s', %s, %s ,'%s', %s, %s)" % \
        (frame.id_camera, frame.id_observation_mode, \
        frame.observation_date, frame.observation_date_microsecond, \
        frame.exposition_time, frame.state, frame.is_raw, \
        frame.program,frame.blockId,frame.path,\
        frame.number_extensions, frame.number_frame, \
        frame.id_principal_investigator, frame.decdeg,frame.radeg)
        try:
            self.cursor.execute(sql)
            frame.id = self.cursor.lastrowid
            logging.debug('The frame has been insert correctly %s %s' %\
            (sql, datetime.now().strftime("%H:%M:%S.%f")))
            return True
        except MySQLdb.Error:
            logging.error('Error while inserting frame %s %s ' %\
            (sql, datetime.now().strftime("%H:%M:%S.%f")))
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
            logging.debug('Created a new header definition called %s %s' %\
            (headerDefinition.name,datetime.now().strftime("%H:%M:%S.%f")))
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
            self.cursor.execute("insert into header(id_frame, extension, "+header.type+") \
            values (%s,%s,%s)", (header.id_frame, header.extension, header.value))
            header.id = self.cursor.lastrowid
            sql2 = "insert into header_definition_header values (%s, %s)" % \
            (headerDefinition.id, header.id)
            self.cursor.execute(sql2)
            logging.debug('Header %s with value %s inserted correctly %s' %\
            (headerDefinition.name, header.value,datetime.now().strftime("%H:%M:%S.%f")))
            return True
        except MySQLdb.Error:
            logging.error('Error while inserting the header %s with value %s %s' %\
            (headerDefinition.name, header.value,datetime.now().strftime("%H:%M:%S.%f")))
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
def setCamera(camera,data):
    camera.instrument = data[0]['INSTRUME'][0]
def setObservationMode(observationMode,data,camera):
    observationMode.id = None
    observationMode.mode = data[0]['OBSMODE'][0]
    observationMode.id_camera = camera.id
def setFrame(frame,data,path,camera, observationMode):
    id_camera = camera  
    raw = isRaw(path)
    program = checkProgramKey(data, path)
    frame.id = None
    frame.id_camera = camera
    frame.id_observation_mode = observationMode
    frame.observation_date = data[0]['DATE'][0]
    frame.observation_date_microsecond = 0
    frame.exposition_time = data[0]['EXPTIME'][0]
    frame.state = 'COMMITED'
    frame.is_raw = raw
    frame.program = data[0][program][0]
    frame.blockId = data[0]['GTCOBID'][0]
    frame.path = path
    frame.number_extensions = len(data)
    frame.number_frame = getNumberFrame(path)
    frame.id_principal_investigator = data[0]['PI'][0]
    frame.decdeg = data[0]['DECDEG'][0]
    frame.radeg = data[0]['RADEG'][0]     
    if frame.blockId == '':
        logging.warning('Block ID is empty %s' % \
        (datetime.now().strftime("%H:%M:%S.%f")))
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

"""
Checks
"""

def isRaw(path):
    path_split = path.rsplit('/')[1:]
    for item in path_split:
        if item == 'raw':
            is_raw=1
            break
    else:
        is_raw=0
    return is_raw
def getDataByPath(keyword, path):
    values = {'INSTRUME' : 5 ,'OBSMODE' : 3,'DATE' : 4}
    path_split = path.rsplit('/')[1:]
    path_ordered = path_split[::-1]
    return path_ordered[values[keyword]]

def checkKeyword(data, path):
    keyword =['INSTRUME','OBSMODE','DATE','EXPTIME','GTCOBID','PI','DECDEG','RADEG']
    for key in keyword:
        try:
            data[0][key] 
        except KeyError:
            if key == 'INSTRUME' or key == 'OBSMODE' or key == 'DATE':
                data[0][key] = [getDataByPath(key, path), '']
            elif key == 'DECDEG' or key == 'RADEG' or key == 'EXPTIME':
                data[0][key] = [0,0]
            else:
                data[0][key] = ['None','None']
            logging.warning('Frame has not Keyword %s %s' % \
            (key,datetime.now().strftime("%H:%M:%S.%f")))


def checkProgramKey(data, path):
    try:
        program_key = 'GTCPRGID'
        data[0][program_key]
    except KeyError:
        program_key = 'GTCPROGI'
        try:
            data[0][program_key]
            logging.warning('The frame has a ProgramId \
key (%s) ambiguous %s' % (program_key,datetime.now().strftime("%H:%M:%S.%f")))
        except KeyError:
            data[0][program_key] = ['', '']
            logging.warning('Frame located in %s has not Keyword %s %s' % \
            (path, program_key,datetime.now().strftime("%H:%M:%S.%f")))
    if data[0][program_key][0] == '':
        logging.warning('%s empty in the frame %s' % \
        (program_key,datetime.now().strftime("%H:%M:%S.%f")))
    return program_key

def getNumberFrame(path):
    path_split = path.rsplit('/')[1:]
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
                    logging.debug('Frame %s open %s' % (final_root, datetime.now().strftime("%H:%M:%S.%f")))
                    Open = startDumpProcess(setModel,DAOs,final_root)
                    logging.debug('Frame %s closed %s' % (final_root, datetime.now().strftime("%H:%M:%S.%f")))
                    if a == 1000:
                        DAOs.db.commit()
                        a=0
    else:
        DAOs.db.commit()              

def startDumpProcess(setModel,DAOs,path):
    data = getDataFitsImages(path)
    checkKeyword(data, path)
    dump = dataBasePopulator(setModel,DAOs,data, path)

def getDataFitsImages(path):
    image = fits.open(path)
    data = []
    for extension in range(len(image)):
        datas = {}
        for keyword in image[extension].header:
            if keyword != 'COMMENT':
                datas[keyword] = [image[extension].header[keyword],\
                image[extension].header.comments[keyword]]
        data.append(datas)
    image.close()
    return data

def dataBasePopulator(setModel,DAOs,data,path):
    logging.debug('Starting dataBasePopulatorHeader %s' % (datetime.now().strftime("%H:%M:%S.%f")))
    dataBasePopulatorFrame(setModel,DAOs,data, path)
    for extension in range(len(data)):
        for keyword in data[extension]:
            dataBasePopulatorHeaderDefinition(setModel,DAOs,data, path,extension,keyword)
            dataBasePopulatorHeader(setModel,DAOs,data, path,extension,keyword)
def dataBasePopulatorFrame(setModel,DAOs,data,path):
    setCamera(setModel.camera, data)
    DAOs.cameraDAO.getId(setModel.camera)
    setObservationMode(setModel.observationMode, data, setModel.camera)
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
    keywordInsertValue = getInsertValue(value)
    headerList = [setModel.headerDefinition.id, setModel.frameData.id, extension,\
    keywordInsertValue, value]
    setHeader(setModel.header,headerList)
    if DAOs.headerDAO.save(setModel.header,setModel.headerDefinition):
        logging.debug('Header with keyword %s and value %s has been inserted correctly %s' % \
        (setModel.headerDefinition.name,value,datetime.now().strftime("%H:%M:%S.%f")))
    else:
        logging.error('Error inserting header %s %s' % \
        (setModel.headerDefinition.name, datetime.now().strftime("%H:%M:%S.%f")))

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
    logging.basicConfig(filename='/home/administrador/log.log',level=logging.DEBUG)
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