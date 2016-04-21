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
        file_name = None
        number_extensions = None
        number_frame = None
        id_principal_investigator = None
        radeg = None
        decdeg = None
        headers = []

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