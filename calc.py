import math, sys

from logger import Logger
# Speed of Sound = 345 m/s = 1130 ft/s = 770 miles/hr

class Calculator:

    # TODO:
    #   1. Add formulas 
    #   2. Connect the formulas to the data store
    def __init__(self, config, data):
        # constant data
        self.logger = Logger(self.__class__.__name__, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        self.configuration = config
        self.data = data


    def update(self):
        '''
        Make all calculations based on the current state.
        '''
        self.logger.debug(sys._getframe().f_code.co_name)
