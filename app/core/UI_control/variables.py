class Variables:
    def __init__(self):
        self.point_cloud_nodes = []
        self.checkboxes = []
        self.labels = []
        self.file_names = []
        self.point_cloud_data = {}
        self.num_layers = 10
        self.saved_gradient_param = None
        self.saved_filter_type = None
        self.saved_min = None
        self.saved_max = None
        self.save_data_h = None
        self.save_data_l = None
        self.slider_timer = None
        self.save_camera_allowed = False
        self.real_max_i = None
        self.real_min_i = None
        self.real_max_u = None
        self.real_min_u = None
        self.real_max_wfs = None
        self.real_min_wfs = None
        self.center = None
        self.point = True
