import tkinter
import sys
from line_widgit import LineWidgit
from logger import Logger

class LowerFrame(tkinter.Frame):
    '''
    This class manages the lower from of the display.
    '''
    def __init__(self, master, data_store):
        self.master = master
        self.data_store = data_store
        self.logger = Logger(self.__class__.__name__, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        self.line_data = []

    def create_frame(self):
        self.logger.debug(sys._getframe().f_code.co_name)
        tkinter.Label(self.master, width=12, text="Hole").grid(row=0, column=0, sticky=tkinter.W)
        tkinter.Label(self.master, width=5, text="Interval").grid(row=0, column=1, sticky=tkinter.W)
        tkinter.Label(self.master, width=10, text="Note").grid(row=0, column=2, sticky=tkinter.W)
        tkinter.Label(self.master, width=10, text="Frequency").grid(row=0, column=3, sticky=tkinter.W)
        tkinter.Label(self.master, width=18, text="Hole Size").grid(row=0, column=4, sticky=tkinter.W)
        tkinter.Label(self.master, width=11, text="Hole Location").grid(row=0, column=5, sticky=tkinter.W)
        tkinter.Label(self.master, width=12, text="Hole Diff").grid(row=0, column=6, sticky=tkinter.W)
        tkinter.Label(self.master, width=12, text="Cutoff Freq").grid(row=0, column=7, sticky=tkinter.W)

        index = self.data_store.bell_note_select
        for n in range(self.data_store.number_holes):
            index += self.data_store.intervals[n]

            # constructed with the minimum data to do a calculation.
            lw = LineWidgit(self.master, self.data_store, n,
                            inter=self.data_store.intervals[n],
                            freq=self.data_store.note_table[index]["frequency"],
                            note=self.data_store.note_table[index]["note"])
            lw.grid(row=n+1, column=0, columnspan=8, sticky=tkinter.W)
            self.data_store.set_line(n, lw)
            #self.data_store.line_data.append(lw)

    def destroy_frame(self):
        #del self.data_store.line_store
        #self.data_store.line_store = []
        self.logger.debug(sys._getframe().f_code.co_name)
        for s in self.master.grid_slaves():
            s.destroy()
        for n in range(self.data_store.number_holes):
            self.data_store.del_line(n)

    def get_state(self):
        '''
        Read the state from the GUI and put it in the data_store.
        '''
        self.logger.debug(sys._getframe().f_code.co_name)
        #return self.data_store.

    def set_state(self, data):
        '''
        Get the state from the data_store and place it into the GUI.
        '''
        self.logger.debug(sys._getframe().f_code.co_name)
        for n in range(self.data_store.number_holes):
            self.data_store.get_line(n).set_state()

    """
    def refresh(self):
        '''
        Take data from the data_store and put it in the display.
        '''
        for n in range(self.data_store.number_holes):
            self.data_store.line_store[n].refresh()

    def store(self):
        '''
        Take data from the display and place it in the data_store.
        '''
        for n in range(self.data_store.number_holes()):
            self.data_store.line_store[n].store()
    """