from tkinter import messagebox
import tkinter
import sys

from data_store import DataStore
#from exception import AppError
#from configuration import Configuration
from hole_widgit import HoleSizeWidgit
from utility import Logger, debugger, raise_event
import utility

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

        self.inter_ctl = tkinter.Entry(self, width=5, validate="focusout", validatecommand=self.change_interval)
        self.inter_ctl.bind('<Return>', self.change_interval)
        self.inter_ctl.bind('<Tab>', self.change_interval)
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
        self.locat_ctl_txt.set("%0.4f"%self.data_store.get_hole_xloc(self.index)) # Label
        self.diff_ctl_txt.set("%0.4f"%self.data_store.get_hole_diff(self.index)) # Label
        self.cutoff_ctl_txt.set("%0.4f"%self.data_store.get_hole_cutoff(self.index)) # Label
        self.hole_ctl.set_state()

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
        self.hole_ctl.get_state()

    @debugger
    def print_state(self):
        self.logger.msg(str(self.get_state()))

    @debugger
    def change_units(self):
        '''
        When this is called, it is assumed that the datastore and the GUI need to have
        the vaules updated to reflect the new units.
        '''
        if self.data_store.get_units():
            self.data_store.set_hole_size(self.index, utility.in_to_mm(self.data_store.get_hole_size(self.index)))
            self.data_store.set_hole_location(self.index, utility.in_to_mm(self.data_store.get_hole_location(self.index)))
            self.data_store.set_hole_diff(self.index, utility.in_to_mm(self.data_store.get_hole_diff(self.index)))
            self.data_store.set_hole_cutoff(self.index, utility.in_to_mm(self.data_store.get_hole_cutoff(self.index)))
        else:
            self.data_store.set_hole_size(self.index, utility.mm_to_in(self.data_store.get_hole_size(self.index)))
            self.data_store.set_hole_location(self.index, utility.mm_to_in(self.data_store.get_hole_location(self.index)))
            self.data_store.set_hole_diff(self.index, utility.mm_to_in(self.data_store.get_hole_diff(self.index)))
            self.data_store.set_hole_cutoff(self.index, utility.mm_to_in(self.data_store.get_hole_cutoff(self.index)))
        self.set_state()
        self.data_store.set_change_flag()

    @debugger
    def change_interval(self, event=None):
        try:
            val = int(self.inter_ctl.get())
            oldval = self.data_store.get_hole_interval(self.index)
            if val != oldval:
                if val > 0 and val < 5:
                    self.data_store.set_hole_interval(self.index, val)
                    self.logger.debug("change interval from %d to %d"%(oldval, val))
                    raise_event("UPDATE_NOTES_EVENT")
                    self.data_store.set_change_flag()
                else:
                    self.logger.error("invalid value for interval: %s"%(str(self.inter_ctl.get())))
                    messagebox.showerror("ERROR", "Intervals must be an integer between 1 and 4")
                    self.inter_ctl.delete(0, tkinter.END)
                    self.inter_ctl.insert(0, str(self.data_store.get_hole_interval(self.index)))
                    return False
            else:
                self.logger.debug("ignore")
        except ValueError:
            self.logger.error("invalid integer for interval: %s"%(str(self.inter_ctl.get())))
            messagebox.showerror("ERROR", "Cannot convert the string \"%s\" to an integer between 1 1nd 4"%(self.inter_ctl.get()))
            self.inter_ctl.delete(0, tkinter.END)
            self.inter_ctl.insert(0, str(self.data_store.get_hole_interval(self.index)))
            return False
        except IndexError:
            pass  # always ignore

        return True