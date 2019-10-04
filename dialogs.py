import tkinter
import utility
from data_store import DataStore

help_text = """
Tilbury Woodwinds Company Whistle Calculator
Chuck Tilbury (c) 2019

This calculator is open source under the MIT and BSD licenses.
"""

class helpDialog:

    def __init__(self, parent):
        self.logger = utility.Logger(self, level=utility.Logger.DEBUG)
        self.logger.debug("enter constructer")

        self.top = tkinter.Toplevel(parent)
        self.tx = tkinter.Text(self.top, height=25, width=80)
        self.sb = tkinter.Scrollbar(self.top)
        self.sb.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.tx.pack(side=tkinter.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        self.tx.insert(tkinter.END, help_text)
        
        self.logger.debug("leave constructer")

