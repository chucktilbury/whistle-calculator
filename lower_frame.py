import tkinter
import sys
import traceback

from data_store import DataStore
from line_widgit import LineWidgit
from utility import Logger, debugger, register_event, raise_event

class LowerFrame(tkinter.Frame):
    '''
    This class manages the lower from of the display.
    '''
    def __init__(self, master):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug("constructor")

        self.data_store = DataStore.get_instance()
        self.master = master
        #self.line_data = []
        self.line_widgits = []
        register_event('UPDATE_LOWER_FRAME_EVENT', self.update_frame)
        register_event('UPDATE_LINES_EVENT', self.set_state)
        register_event('UPDATE_NOTES_EVENT', self.update_notes)
        register_event('CHANGE_UNITS_EVENT', self.change_units)

        tkinter.Label(self.master, width=12, text="Hole").grid(row=0, column=0, sticky=tkinter.W)
        tkinter.Label(self.master, width=5, text="Interval").grid(row=0, column=1, sticky=tkinter.W)
        tkinter.Label(self.master, width=10, text="Note").grid(row=0, column=2, sticky=tkinter.W)
        tkinter.Label(self.master, width=10, text="Frequency").grid(row=0, column=3, sticky=tkinter.W)
        tkinter.Label(self.master, width=18, text="Hole Size").grid(row=0, column=4, sticky=tkinter.W)
        tkinter.Label(self.master, width=11, text="Hole Location").grid(row=0, column=5, sticky=tkinter.W)
        tkinter.Label(self.master, width=12, text="Hole Diff").grid(row=0, column=6, sticky=tkinter.W)
        tkinter.Label(self.master, width=12, text="Cutoff Freq").grid(row=0, column=7, sticky=tkinter.W)

        # create all of the lines
        for n in range(12):
            lw = LineWidgit(self.master, n)
            self.line_widgits.append(lw)

        for idx in range(self.data_store.get_number_holes()):
            self.line_widgits[idx].grid(row=idx+1, column=0, columnspan=8, sticky=tkinter.W)
            self.line_widgits[idx].set_state()

        self.logger.debug("end constructor")

    @debugger
    def update_frame(self):
        # hide all of the lines
        for idx in range(12):
            self.line_widgits[idx].grid_forget()

        # expose the correct number of lines
        for idx in range(self.data_store.get_number_holes()):
            self.line_widgits[idx].grid(row=idx+1, column=0, columnspan=8, sticky=tkinter.W)
            self.line_widgits[idx].set_state()

        self.update_notes()
        
    @debugger
    def set_state(self):
        '''
        Copy data from the datastore into all lines in GUI
        '''
        for line in self.line_widgits:
            line.set_state()

    @debugger
    def get_state(self):
        '''
        Copy data from the line widgits into the data_store
        '''
        for line in self.line_widgits:
            line.get_state()

    @debugger
    def update_notes(self):
        sel = self.data_store.get_bell_note_select()
        for index, line in enumerate(self.line_widgits): 
            sel += self.data_store.get_hole_interval(index)
            self.data_store.set_hole_freq(index, self.data_store.note_table[sel]["frequency"])
            self.data_store.set_hole_note(index, self.data_store.note_table[sel]["note"])
            line.set_state()
        raise_event("CALCULATE_EVENT")


    @debugger
    def change_units(self):
        '''
        When this is called, it is assumed that the data_store has the wrong 
        units. The values are converted to the current units and the GUI
        is updated.
        '''
        for line in self.line_widgits:
            line.change_units()
