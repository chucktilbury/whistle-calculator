from tkinter import messagebox
import tkinter
import sys, math

from data_store import DataStore
#from configuration import Configuration
from utility import Logger, debugger, register_event
from exception import AppError, AppFatalError
import utility

class HoleSizeWidgit(tkinter.Frame):

    def __init__(self, parent, line):
        '''
        This is a specialized widget to track the hole diameter. It displays 
        the value according to the state. It has up and down buttons used to
        increment or decrement the value. 
        '''
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug("constructor")
        self.index = line

        tkinter.Frame.__init__(self, parent)
        self.data_store = DataStore.get_instance()

        BITMAP_UP = """
            #define up_width 9
            #define up_height 5
            static unsigned char up_bits[] = {
                0x10, 0x00, 0x38, 0x00, 0x7c, 0x00, 0xfe, 0x00, 0xff, 0x01 };
            """

        BITMAP_DOWN = """
            #define down_width 9
            #define down_height 5
            static unsigned char down_bits[] = {
                0xff, 0x01, 0xfe, 0x00, 0x7c, 0x00, 0x38, 0x00, 0x10, 0x00 };
        """

        # TODO: Put these constants into a configuration file.
        #       Need to resolve the mm/inch question for configurations.
        #       Track it separately? Or just change the values?
        # self.inc = 1/64
        # self.max = 1/2
        # self.min = 3/32
        # self.value = 11/32
        # self.fracs = True # display as fractions if true
        # self.mm_in = False # calculate as mm if true

        self.entry = tkinter.Entry(self, width=25-18)
        #self.entry.insert(0, default)

        self.entry.grid(row=0, column=1, rowspan=2)

        self.bitmap_up = tkinter.BitmapImage(data=BITMAP_UP, foreground="black", background="white")
        self.b1 = tkinter.Button(self, text="up", image=self.bitmap_up, command=self.incr_command)
        self.b1.grid(row=0, column=2)
        self.b1.config(width=9, height=5)

        self.bitmap_down = tkinter.BitmapImage(data=BITMAP_DOWN)
        self.b2 = tkinter.Button(self, image=self.bitmap_down, command=self.decr_command)
        self.b2.grid(row=1, column=2)
        self.b2.config(width=9, height=5)
        
        register_event("UPDATE_HOLE_EVENT", self.update_val)
        self.set_state()

        self.logger.debug("constructor return")

    @debugger
    def get_state(self):
        '''
        Put the current value into the data_store.
        '''
        try:
            if self.fracs:
                self.value = utility.fractof(self.entry.get())
            else:
                self.value = float(self.entry.get())
        except ValueError as e:
            raise AppError('get_state', 'Cannot convert hole to float: %s'%(self.entry.get()), e)

        line = self.data_store.get_line(self.index)
        line['hole_size'] = self.value
        self.data_store.set_line(self.index, line)

    @debugger
    def update_state(self):
        try:
            if self.data_store.get_units(): # if true then metric
                self.inc = self.data_store.get_hole_mm_inc()
                self.max = self.data_store.get_hole_mm_max()
                self.min = self.data_store.get_hole_mm_min()
            else:
                self.inc = self.data_store.get_hole_in_inc()
                self.max = self.data_store.get_hole_in_max()
                self.min = self.data_store.get_hole_in_min()
            self.fracs = self.data_store.get_disp_frac()
            self.units = self.data_store.get_units()
            self.value = self.data_store.get_line(self.index)['hole_size']

        except AppFatalError as e:
            e.show()
        except Exception as e:
            raise AppFatalError(str(e), 'HoleSizeWidgit.set_state')

    @debugger
    def set_state(self):
        '''
        Get the current state from the data_store
        '''
        self.update_state()
        self.update_val()   # display the new state

    @debugger
    def update_val(self):
        self.update_state()
        self.entry.delete(0, tkinter.END)
        if not self.units:
            self.logger.debug("updating inch value to %s"%(str(self.value)))
            if self.fracs:
                self.entry.insert(0, "%s"%(utility.reduce(self.value)))
            else:
                self.entry.insert(0, "%0.3f"%(self.value))
        else:
            self.logger.debug("updating mm value to %s"%(str(self.value)))
            self.entry.insert(0, "%0.3f"%(self.value))
            

    # event handlers
    @debugger
    def incr_command(self):
        self.value = self.value + self.inc
        if self.value > self.max:
            self.value = self.max
        self.update_val()

    @debugger
    def decr_command(self):
        self.value = self.value - self.inc
        if self.value < self.min:
            self.value = self.min
        self.update_val()

    def print_state(self):
        self.logger.msg(str(self.get_state()))
