import math, sys

from data_store import DataStore
#from configuration import Configuration
from utility import Logger, debugger, register_event

# Speed of Sound = 345 m/s = 1130 ft/s = 770 miles/hr

class Calculator:

    # TODO:
    #   1. Add formulas 
    #   2. Connect the formulas to the data store
    def __init__(self):
        # constant data
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug("enter constructor")
        #self.configuration = Configuration.get_instance()
        self.data = DataStore.get_instance()
        self.logger.debug("end constructor")
        register_event("CALCULATE_EVENT", self.do_calc)


    @debugger
    def update(self):
        '''
        Make all calculations based on the current state.
        '''
        pass

    @debugger
    def do_calc(self):
        pass
