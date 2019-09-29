from tkinter import messagebox
import tkinter
import sys

from data_store import DataStore
#from configuration import Configuration
from hole_widgit import HoleSizeWidgit
from utility import Logger, debugger

class LineWidgit(tkinter.Frame):
    '''
    This is the GUI widget that represents a single line in the output
    data. It uses the data_store to communicate values into and out of
    itself.
    '''

    def __init__(self, parent,lineno):
        self.logger = Logger(self, Logger.ERROR)
        self.logger.debug("constructor")
        tkinter.Frame.__init__(self, parent)

        self.data_store = DataStore.get_instance()
        self.index = lineno

        self.name = "Hole %d" % (lineno+1)
        self.line_name = tkinter.Label(self, text=self.name, width=12)
        self.line_name.grid(row=lineno+1, column=0, sticky=tkinter.W)

        self.inter_ctl = tkinter.Entry(self, width=5, validate="focusout")#, validatecommand=self.numHolesCommand)
        self.inter_ctl.grid(row=lineno+1, column=1)

        self.note_ctl_txt = tkinter.StringVar()
        self.note_ctl = tkinter.Label(self, textvariable=self.note_ctl_txt, width=12)
        self.note_ctl.grid(row=lineno+1, column=2)

        self.freq_ctl_txt = tkinter.StringVar()
        self.freq_ctl = tkinter.Label(self, textvariable=self.freq_ctl_txt, width=12)
        self.freq_ctl.grid(row=lineno+1, column=3)

        self.hole_ctl = HoleSizeWidgit(self, lineno)
        self.hole_ctl.config(padx=25)
        self.hole_ctl.grid(row=lineno+1, column=4)

        self.locat_ctl_txt = tkinter.StringVar()
        self.locat_ctl = tkinter.Label(self, textvariable=self.locat_ctl_txt, width=12)
        self.locat_ctl.grid(row=lineno+1, column=5)

        self.diff_ctl_txt = tkinter.StringVar()
        self.diff_ctl = tkinter.Label(self, textvariable=self.diff_ctl_txt, width=12)
        self.diff_ctl.grid(row=lineno+1, column=6)

        self.cutoff_ctl_txt = tkinter.StringVar()
        self.cutoff_ctl = tkinter.Label(self, textvariable=self.cutoff_ctl_txt, width=12)
        self.cutoff_ctl.grid(row=lineno+1, column=7)

        self.set_state()

        self.logger.debug("end constructor")

    @debugger
    def set_state(self):
        '''
        Place the data from the data_store into the GUI.
        '''
        self.inter_ctl.delete(0, tkinter.END)
        self.inter_ctl.insert(0, str(self.data_store.get_hole_interval(self.index)))
        self.note_ctl_txt.set(str(self.data_store.get_hole_note(self.index))) # Label
        self.freq_ctl_txt.set("%s Hz"%(str(self.data_store.get_hole_freq(self.index))))
        self.locat_ctl_txt.set(str(self.data_store.get_hole_location(self.index))) # Label
        self.diff_ctl_txt.set(str(self.data_store.get_hole_diff(self.index))) # Label
        self.cutoff_ctl_txt.set(str(self.data_store.get_hole_cutoff(self.index))) # Label

    @debugger
    def get_state(self):
        '''
        Get the data out of the display and place it in the data_store.
        '''
        self.data_store.set_hole_interval(self.index, int(self.inter_ctl.get()))
        self.data_store.set_hole_note(self.index, self.note_ctl_txt.get()) # str
        self.data_store.set_hole_freq(self.index, float(self.freq_ctl_txt.get().split()[0]))
        self.data_store.set_hole_location(self.index, float(self.locat_ctl_txt.get()))
        self.data_store.set_hole_diff(self.index, float(self.diff_ctl_txt.get()))
        self.data_store.set_hole_cutoff(self.index, float(self.cutoff_ctl_txt.get()))

    @debugger
    def print_state(self):
        self.logger.msg(str(self.get_state()))

    @debugger
    def convert_units(self, units):
        '''
        Convert from one inch or metric units to the other
        '''
        #self.hole_ctl.change_units(units)
        # TODO: change the other measurements into the new units.

