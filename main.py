#!/usr/bin/python3

import tkinter
from main_frame import MainFrame

if __name__ == "__main__":
    top = tkinter.Tk()
    app = MainFrame(top)
    top.wm_title("Whistle Calculator")
    top.mainloop()
