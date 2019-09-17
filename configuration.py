import sys

from logger import Logger

class Configuration:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        self.load('somefile.cfg')

        # line defaults
        self.mm_in = False
        self.in_inc = 1/64
        self.in_max = 1/2
        self.in_min = 3/32
        self.in_value = 11/32
        self.mm_inc = 0.5
        self.mm_max = 12.5
        self.mm_min = 2.5
        self.mm_value = 9.0

        # upper defaults
        self.title = "Default Whistle"
        self.inside_dia = 0.5
        self.num_holes = 6
        self.emb_area = 1.2
        self.units = False
        self.wall_thick = 0.15
        self.bell_select = 62
        self.format = True


    def load(self, fname):
        self.logger.debug(sys._getframe().f_code.co_name)

    def save(self, fname):
        self.logger.debug(sys._getframe().f_code.co_name)

    def get(self):
        self.logger.debug(sys._getframe().f_code.co_name)