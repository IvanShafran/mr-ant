from PySide.QtCore import QPoint


class RunToAnthillSettings():
    def __init__(self):
        self.focus_point = QPoint(0, 0)
        self.width = 0
        self.height = 0
        self.number_of_barriers = 0
        self.number_of_background_pictures = 0
        self.number_of_ants = 0
        self.number_of_zombie_ants = 0
        self.start_line_x = 0
        self.finish_line_x = 0
        self.screen_movement_step = 0
        self.distance_before_first_barrier = 0
        self.critical_distance_before_screen_end = 0
