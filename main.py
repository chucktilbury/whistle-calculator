#!/usr/bin/python3

import tkinter
import traceback, sys
from main_frame import MainFrame
from utility import Logger
#from data_store import DataStore
#from configuration import Configuration

if __name__ == "__main__":

    try:
        logger = Logger(__name__, Logger.INFO)
        logger.debug(sys._getframe().f_code.co_name)

        top = tkinter.Tk()
        app = MainFrame(top)
        top.wm_title("Whistle Calculator")

        logger.debug("start main loop")
        top.mainloop()
        logger.debug("end main loop")

    except Exception as e:
        traceback.print_exception(*sys.exc_info())

