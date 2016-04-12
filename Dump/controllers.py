"""
Models:
"""

class Camera(object):
    def __init__(self):
        self.id = None
        self.instrument = None
        self.camera = None
        self.gcs_component = None
        self.display_name = None
        self.archive_directory = None
        self.active = None

class ObservationMode(object):
    def __init__(self):
        id = None
        mode = None
        id_camera = None     

class Frame(object):
    def __init__(self):
        id = None
        id_camera = None
        id_observation_mode = None
        observation_date = None
        observation_date_microsecond = None
        exposition_time = None
        state = None
        is_raw = None
        id_program = None
        id_observation_block = None
        path = None
        id_principal_investigator = None
        radeg = None
        decdeg = None

class HeaderDefinition(object):
    def __init__(self):
        id = None
        comment = None
        name = None
        data_type = None
        visible = None
        id_observation_mode = None

class Header(object):
    def __init__(self):
        id = None
        id_header_definition = None
        id_frame = None
        extension = None
        string_value = None
        long_value = None
        double_value = None

"""
DAO
""" 
class CameraDAO(object):
    def __init__(cursor):
        cursor = cursor
    def getId(camera):
        cursor.execute("select id from camera where instrument = '"+camera.instrument+"'")
        results = cursor.fetchall()
        for row in results:
            id_camera = row[0]
        camera.id = id_camera

class ObservationModeDAO(object):
    def __init__(cursor):
        cursor = cursor
    def getId(observationMode):
        cursor.execute("select id, id_camera from observation_mode \
        where mode = '"+mode+"'")
        results = cursor.fetchall()
        for row1 in results:
            observationMode.id = row1[0]
            observationMode.mode = mode
            observationMode.id_camera = row1[1]
            return True
            break
        else:
            self.id = False
    def save(observationMode):
        if cursor.execute("insert into observation_mode(mode,id_camera) \
        values (%s,%s)", (observationMode.mode, observationMode.id_camera)):
            return True
        else:
            return False 

class FrameDAO(object):
    def __init__(cursor):
        cursor = cursor
    def save(frame):
        if cursor.execute("insert into frame(id_camera, id_observation_mode, \
        observation_date, observation_date_microsecond, exposition_time,state,is_raw, \
        id_program, id_observation_block,path, id_principal_investigator, decdeg, \
        radeg) values (%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)", \
        (frame.id_camera, frame.id_observation_mode, \
        frame.observation_date, frame.observation_date_microsecond, \
        frame.exposition_time, frame.state, frame.is_raw, \
        frame.program,frame.blockId,frame.path,\
        frame.id_principal_investigator, frame.decdeg,frame.radeg)):
            frame.id = cursor.lastrowid
            logging.debug('The frame %s has been insert correctly'+now, frame.path)
            return True
        else:
            logging.warning('Error while inserting frame %s '+now, frame.path)
            return False

class HeaderDefinitionDAO(object):
    def __init__(cursor):
        cursor = cursor
    def getId(headerDefinition):
        cursor.execute("select id from header_definition where comment = %s and \
        name= %s and data_type = %s and id_observation_mode = %s", \
        (headerDefinition.comment,headerDefinition.name, headerDefinition.data_type, headerDefinition.id_observation_mode))
        results = cursor.fetchall()
        if len(results) > 0:
            for row in results:
                headerDefinition.id = row[0]
                break
        else:
            return False
    def save(headerDefinition):
        if cursor.execute("insert into header_definition(comment, name, data_type, \
        visible, id_observation_mode) values (%s,%s,%s,1,%s)", (headerDefinition.comment, \
        headerDefinition.name, headerDefinition.data_type, headerDefinition.id_observation_mode)):
            logging.debug('Created a new header definition called %s at %s' %\
            (headerDefinition.name,now))
            return True
        else:
            logging.warning('Error while creating a new header definition %s'+now)
            return False
class HeaderDAO(object):
    def __init__(cursor):
        cursor = cursor
    def save(header):
        if cursor.execute("insert into header(id_header_definition, id_frame, \
        extension, "+header.type+") values (%s,%s,%s,%s)", \
        (header.id_header_definition, header.id_frame, header.extension, header.value)):
            return True
        else:
            False

"""
Set
"""
def setCamera(camera,instrument):
    camera.instrument = instrument
def setObservationMode(observationMode,mode,idCamera):
    observationMode.id = None
    observationMode.mode = mode
    observationMode.id_camera = idCamera
def setFrame(frame,data,path):
    mode = data[0]['OBSMODE'][0]
    camera = CameraDAO()
    camera.getId(data[0]['INSTRUME'][0])
    observationMode = ObservationModeDAO()
    observationMode.getId(mode)
    if observationMode.id == False:
        setObservationMode(observationMode, mode, camera.id)
        observationMode.save()
        observationMode.getId(mode)
        logging.info('A new Observation Mode named %s has been created  %s' % \
        (mode,now))
    raw = isRaw(path)
    program = checkProgramKey(data, path)
    frame.id = None
    frame.id_camera = camera.id
    frame.id_observation_mode = observationMode.id
    frame.observation_date = data[0]['DATE'][0]
    frame.observation_date_microsecond = 0
    frame.exposition_time = data[0]['ELAPSED'][0]
    frame.state = 'COMMITED'
    frame.is_raw = raw
    frame.program = data[0][program][0]
    frame.blockId = data[0]['GTCOBID'][0]
    frame.path = path
    frame.id_principal_investigator = data[0]['PI'][0]
    frame.decdeg = data[0]['DECDEG'][0]
    frame.radeg = data[0]['RADEG'][0]     
    if frame.blockId == '':
        logging.warning('Block ID is empty in %s %s' % (path, now))
    return frame

def setHeaderDefinition(headerDefinitionData, headerData):
        headerDefinitionData.id = None
        headerDefinitionData.comment = headerData[0]
        headerDefinitionData.name = headerData[1]
        headerDefinitionData.data_type = headerData[2]
        headerDefinitionData.visible = 1
        headerDefinitionData.id_observation_mode = headerData[3]

def setHeader(headerData, headerList):
        headerData.id = None
        headerData.id_header_definition = headerList[0]
        headerData.id_frame = headerList[1]
        headerData.extension = headerList[2]
        headerData.type = headerList[3]
        headerData.value = headerList[4]

"""
Checks
"""

def isRaw(path):
    path_split = path.rsplit('/')[1:]
    if path_split[6] == 'raw':
        is_raw=1
    else:
        is_raw=0
    return is_raw

def checkProgramKey(data, path):
    try:
        program_key = 'GTCPRGID'
        data[0][program_key]
    except KeyError:
        program_key = 'GTCPROGI'
        data[0][program_key]
        logging.warning('The frame located in %s has a ProgramId \
        key ambiguous %s' % (path, now))
    if data[0][program_key][0] == '':
        logging.warning('%s empty in the frame located in %s %s' % \
        (program_key, path,now))
    return program_key

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
class Controller(object):
    def db(self):
        self.db = MySQLdb.connect("localhost", "root", "", "datafactory")
        self.cursor = db.cursor()
    def DAO(self):
        self.frameDAO = FrameDAO(self.cursor)
        self.cameraDAO = CameraDAO(sel.cursor)
        self.observationModeDAO = ObservationModeDAO(sel.cursor)
        self.headerDefinitionDAO = HeaderDefinitionDAO(sel.cursor)
        self.headerDAO = HeaderDAO(sel.cursor)
    def startScript(self,args):
        route = args.route
        scan = args.scan
        default = args.default
        filepath, fileextension = os.path.splitext(route)
        if scan == True and fileextension == '': 
            start = fileScaner(default, route)
        elif scan != True and fileextension != '':
            start = startDumpProcess(route)
            db.commit()

    def fileScaner(self,pathRoot,path1):
        path = pathRoot+path1
        yu = glob.glob(path)
        for dire in yu:
            for root, dirs, files in os.walk(dire):
                for fil in files:
                    if fil.endswith(".fits"):
                        final_root = (os.path.join(root,fil))
                        Open = startDumpProcess(final_root)
            db.commit()

    def startDumpProcess(self,path):
        data = getDataFitsImages(path)
        dump = dataBasePopulator(data, path)
       
    def getDataFitsImages(self,path):
        image = fits.open(path)
        data = []
        for extension in range(len(image)):
            datas = {}
            for keyword in image[extension].header:
                datas[keyword] = [image[extension].header[keyword],\
                image[extension].header.comments[keyword]]
            data.append(datas)
        image.close()
        return data

    def dataBasePopulator(self,data, path):
        frameData = Frame() 
        setFrame(frameData, data, path)
        self.frameDAO.save(frameData)
        headerDefinition = HeaderDefinition()
        header = Header()
        for extension in range(len(data)):
            for keyword in data[extension]:
                value = data[extension][keyword][0]
                observationModeId = frameData.id_observation_mode
                keywordType = getKeywordType(value)
                headerDefList = [data[extension][keyword][1],keyword,\
                keywordType,observationModeId]
                setHeaderDefinition(headerDefinition,headerDefList)
                if self.headerDefinitionDAO.getId(headerDefinition) == False:
                    self.headerDefinitionDAO.save(headerDefinition)
                    self.headerDefinitionDAO.getId(headerDefinition)
                keywordInsertValue = getInsertValue(value)
                headerList = [self.headerDefinition.id, frameData.id, extension,\
                keywordInsertValue, value]
                setHeader(header,headerList)
                self.headerDAO.save(headerData)

if __name__ == '__main__':
    from astropy.io import fits
    import argparse
    import os
    import time
    import logging
    import sys
    import MySQLdb
    import glob
    
    logging.basicConfig(filename='/home/log.log',level=logging.DEBUG)
    now = time.strftime("%c")
    parser = argparse.ArgumentParser(description="Do you wish to scan?")
    parser.add_argument("-r", dest='route', action='store',help='Route\
    of the instrument and the date that you want to dump')
    parser.add_argument("-s", dest='scan', action='store',\
    help='Scan files in a directory', default=True)
    parser.add_argument("-d", dest='default', action='store',\
    help='Use default route', default='/scidb/framedb/')
    args = parser.parse_args()
    p1 = Controller(args)
    db.close() 