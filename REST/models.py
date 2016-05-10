class Camera(object):
    def __init__(self):
        self.id = None
        self.instrument = None
        self.camera = None
        self.gcsComponent = None
        self.displayName = None
        self.archiveDirectory = None
        self.active = None

class ObservationMode(object):
    def __init__(self):
        self.id = None
        self.mode = None
        self.idCamera = None     

class Frame(object):
    def __init__(self):
        self.id = None
        self.camera = []
        self.observationMode = None
        self.observationDate = None
        self.observationDateMicrosecond = None
        self.exposureTime = None
        self.state = None
        self.isRaw = None
        self.programId = None
        self.observationBlockId = None
        self.path = None
        self.fileName = None
        self.numberExtensions = None
        self.numberFrame = None
        self.piName = None
        self.radeg = None
        self.decdeg = None
        self.observationDateUsec = []
        self.fitsKeywords=[]

class HeaderDefinition(object):
    def __init__(self):
        self.id = None
        self.comment = None
        self.name = None
        self.version = None
        self.dataType = None
        self.visible = None
        self.obsMode = None

class Header(object):
    def __init__(self):
        self.id = None
        self.idFrame = None
        self.orderKeyword = None
        self.extension = None
        self.stringVal = None
        self.longVal = None
        self.doubleVal = None
        self.fitsKeywordsDef = []