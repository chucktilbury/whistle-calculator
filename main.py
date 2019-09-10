#!/usr/bin/python3

import tkinter
from main_frame import MainFrame
from logger import Logger

if __name__ == "__main__":

    logger = Logger("whistle calc main")
    logger.info("starting")
    top = tkinter.Tk()
    app = MainFrame(top)
    top.wm_title("Whistle Calculator")
    logger.info("start main loop")
    top.mainloop()
    logger.info("end main loop")
