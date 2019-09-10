import math

from logger import Logger
# Speed of Sound = 345 m/s = 1130 ft/s = 770 miles/hr

class Calculator:

    def __init__(self, data):
        # constant data
        self.logger = Logger("Calculator", Logger.DEBUG)
        self.data = data
        self.logger.debug("constructor")


    def update(self):
        '''
        Make all calculations based on the current state.
        '''
        self.logger.debug("update")
