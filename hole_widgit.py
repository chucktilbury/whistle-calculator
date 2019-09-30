from tkinter import messagebox
import tkinter
import sys, math

from data_store import DataStore
#from configuration import Configuration
from utility import Logger, debugger, register_event, raise_event
from exception import AppError, AppFatalError
import utility

class HoleSizeWidgit(tkinter.Frame):

    def __init__(self, parent, line):
        '''
        This is a specialized widget to track the hole diameter. It displays 
        the value according to the state. It has up and down buttons used to
        increment or decrement the value. 
        '''
        self.logger = Logger(self, Logger.INFO)
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

        self.entry = tkinter.Entry(self, width=25-18)
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
            if self.data_store.get_disp_frac():
                val = utility.fractof(self.entry.get())
            else:
                val = float(self.entry.get())
        except ValueError as e:
            raise AppError('get_state', 'Cannot convert hole to float: %s'%(self.entry.get()), e)

        self.data_store.set_hole_size(self.index, val)

    @debugger
    def set_state(self):
        '''
        Get the current state from the data_store and place it in the GUI
        '''
        self.update_val()   # display the new state

    @debugger
    def update_val(self):
        siz = self.data_store.get_hole_size(self.index)
        self.entry.delete(0, tkinter.END)
        if not self.data_store.get_units():
            self.logger.debug("updating inch value to %s"%(str(siz)))
            if self.data_store.get_disp_frac():
                self.entry.insert(0, "%s"%(utility.reduce(siz)))
            else:
                self.entry.insert(0, "%0.3f"%(siz))
        else:
            self.logger.debug("updating mm value to %s"%(str(siz)))
            self.entry.insert(0, "%0.3f"%(siz))

    # event handlers
    @debugger
    def incr_command(self):
        siz = self.data_store.get_hole_size(self.index)
        siz = siz + self.data_store.get_hole_inc()

        if siz > self.data_store.get_hole_max():
            siz = self.data_store.get_hole_max()
        elif siz < self.data_store.get_hole_min():
            siz = self.data_store.get_hole_min()

        self.data_store.set_hole_size(self.index, siz)
        self.update_val() # update the GUI
        raise_event("CALCULATE_EVENT")

    @debugger
    def decr_command(self):
        siz = self.data_store.get_hole_size(self.index)
        siz = siz - self.data_store.get_hole_inc()

        if siz < self.data_store.get_hole_min():
            siz = self.data_store.get_hole_min()
        elif siz > self.data_store.get_hole_max():
            siz = self.data_store.get_hole_max()

        self.data_store.set_hole_size(self.index, siz)
        self.update_val() # update the GUI
        raise_event("CALCULATE_EVENT")


    def print_state(self):
        self.logger.msg(str(self.get_state()))
