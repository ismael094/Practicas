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
        id = None
        mode = None
        idCamera = None     

class Frame(object):
    def __init__(self):
        id = None
        idCamera = None
        idObservationMode = None
        observationDate = None
        observationDateMicrosecond = None
        expositionTime = None
        state = None
        isRaw = None
        idProgram = None
        idObservation_block = None
        path = None
        fileName = None
        numberExtensions = None
        numberFrame = None
        idPrincipalInvestigator = None
        radeg = None
        decdeg = None
        header=[]

class HeaderDefinition(object):
    def __init__(self):
        id = None
        comment = None
        name = None
        dataType = None
        visible = None
        idObservationMode = None

class Header(object):
    def __init__(self):
        id = None
        idHeaderDefinition = None
        idFrame = None
        extension = None
        stringValue = None
        longValue = None
        doubleValue = None