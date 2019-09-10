#!/usr/bin/python3

import tkinter
import traceback, sys
from main_frame import MainFrame
from logger import Logger

if __name__ == "__main__":

    try:
        logger = Logger("whistle calc main")
        logger.debug("starting")
        
        top = tkinter.Tk()
        app = MainFrame(top)
        top.wm_title("Whistle Calculator")

        logger.debug("start main loop")
        top.mainloop()
        logger.debug("end main loop")

    except Exception as e:
        traceback.print_exception(*sys.exc_info())

