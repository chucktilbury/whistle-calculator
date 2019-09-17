import sys

from logger import Logger

class Configuration:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)

    def load(self, fname):
        self.logger.debug(sys._getframe().f_code.co_name)

    def save(self, fname):
        self.logger.debug(sys._getframe().f_code.co_name)

    def get(self):
        self.logger.debug(sys._getframe().f_code.co_name)