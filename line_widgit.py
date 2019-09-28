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

    def __init__(self, 
                    parent,
                    lineno,
                    inter=0,
                    note="",
                    freq=0.0,
                    hole_size=0.0,
                    location=0.0,
                    cutoff=0.0,
                    diff=0.0,
                    units=False,
                    fracs=True):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug("constructor")
        tkinter.Frame.__init__(self, parent)

        #self.configuration = Configuration.get_instance()
        self.data_store = DataStore.get_instance()
        self.index = lineno

        self.name = "Hole %d" % (lineno+1)
        self.line_name = tkinter.Label(self, text=self.name, width=12)
        self.line_name.grid(row=lineno+1, column=0, sticky=tkinter.W)

        self.inter_ctl = tkinter.Entry(self, width=5, validate="focusout")#, validatecommand=self.numHolesCommand)
        self.inter_ctl.delete(0, tkinter.END)
        self.inter_ctl.insert(0, str(inter))
        self.inter_ctl.grid(row=lineno+1, column=1)

        self.note_ctl_txt = tkinter.StringVar()
        self.note_ctl_txt.set(str(note))
        self.note_ctl = tkinter.Label(self, textvariable=self.note_ctl_txt, width=12)
        self.note_ctl.grid(row=lineno+1, column=2)

        self.freq_ctl_txt = tkinter.StringVar()
        self.freq_ctl_txt.set("%s Hz"%(str(freq)))
        self.freq_ctl = tkinter.Label(self, textvariable=self.freq_ctl_txt, width=12)
        self.freq_ctl.grid(row=lineno+1, column=3)

        self.hole_ctl = HoleSizeWidgit(self, lineno)
        self.hole_ctl.config(padx=25)
        self.hole_ctl.grid(row=lineno+1, column=4)

        # TODO: 
        #   1, Move these default values to the data-store and allow them to be configured
        #      via a configuration file.
        # data = self.hole_ctl.get_state() # get a copy of the state
        # data['units'] = units
        # data['fracs'] = fracs
        # data['value'] = hole_size
        # if units:
        #     data['inc'] = self.data_store.get_hole_mm_inc()
        #     data['min'] = self.data_store.get_hole_mm_min()
        #     data['max'] = self.data_store.get_hole_mm_max()
        # else:
        #     data['inc'] = self.data_store.get_hole_in_inc()
        #     data['min'] = self.data_store.get_hole_in_min()
        #     data['max'] = self.data_store.get_hole_in_max()
        # self.hole_ctl.set_state(data)

        self.locat_ctl_txt = tkinter.StringVar()
        self.locat_ctl_txt.set(str(location))
        self.locat_ctl = tkinter.Label(self, textvariable=self.locat_ctl_txt, width=12)
        self.locat_ctl.grid(row=lineno+1, column=5)

        self.diff_ctl_txt = tkinter.StringVar()
        self.diff_ctl_txt.set(str(diff))
        self.diff_ctl = tkinter.Label(self, textvariable=self.diff_ctl_txt, width=12)
        self.diff_ctl.grid(row=lineno+1, column=6)

        self.cutoff_ctl_txt = tkinter.StringVar()
        self.cutoff_ctl_txt.set(str(cutoff))
        self.cutoff_ctl = tkinter.Label(self, textvariable=self.cutoff_ctl_txt, width=12)
        self.cutoff_ctl.grid(row=lineno+1, column=7)

        #self.get_data()

    @debugger
    def set_state(self):
        '''
        Place the data from the data_store into the GUI.
        '''
        line = self.data_store.get_line(self.index)
        self.inter_ctl.delete(0, tkinter.END)
        self.inter_ctl.insert(0, str(line['interval']))
        self.note_ctl_txt.set(str(line['note'])) # Label
        self.freq_ctl_txt.set("%s Hz"%(str(line['freq'])))
        self.locat_ctl_txt.set(str(line['location'])) # Label
        self.diff_ctl_txt.set(str(line['diff'])) # Label
        self.cutoff_ctl_txt.set(str(line['cutoff'])) # Label
        #self.hole_ctl.set_state(line['hole_size'])
        self.hole_ctl.set_state()

        #self.hole_ctl.set_startval(data['hole']) # HoleWidgit
        #self.hole_ctl.set_state(data['hole']) # HoleWidgit

    @debugger
    def get_state(self):
        '''
        Get the data out of the display and place it in the data_store.
        '''
        line = self.data_store.get_line(self.index)
        line['interval'] = int(self.inter_ctl.get())
        line['note'] = self.note_ctl_txt.get() # str
        line['freq'] = float(self.freq_ctl_txt.get().split()[0])
        #line['hole_size'] = float(self.hole_ctl.get_state())
        line['location'] = float(self.locat_ctl_txt.get())
        line['diff'] = float(self.diff_ctl_txt.get())
        line['cutoff'] = float(self.cutoff_ctl_txt.get())
        self.hole_ctl.get_state()
        line = self.data_store.set_line(self.index, line)

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

