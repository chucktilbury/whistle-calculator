import tkinter
import sys
from tkinter import messagebox
from tkinter import ttk

from data_store import DataStore
#from configuration import Configuration
from utility import Logger, debugger, raise_event

class UpperFrame(tkinter.Frame):
    '''
    This class manages the upper frame of the display.
    '''
    def __init__(self, master):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug("constructor")
        self.master = master
        self.data_store = DataStore.get_instance()

    @debugger
    def create_frame(self):
        # build the screen

        # Fill in the upper frame
        tkinter.Label(self.master, text="Title").grid(row=0, column=0, sticky=tkinter.E)
        self.titleEntry = tkinter.Entry(self.master, width=40)
        self.titleEntry.grid(row=0, column=1, columnspan=3, padx=9, pady=4)

        tkinter.Label(self.master, text="Inside Diameter").grid(row=1, column=0, sticky=tkinter.E, pady=4)
        self.insideDiaEntry = tkinter.Entry(self.master, validate="focusout", validatecommand=self.insideDiaCommand)
        self.insideDiaEntry.bind('<Return>', self.insideDiaCommand)
        self.insideDiaEntry.bind('<Tab>', self.insideDiaCommand)
        self.insideDiaEntry.grid(row=1, column=1, pady=4)

        tkinter.Label(self.master, text="Wall Thickness").grid(row=1, column=2, sticky=tkinter.E, pady=4)
        self.wallThicknessEntry = tkinter.Entry(self.master, validate="focusout", validatecommand=self.wallThicknessCommand)
        self.wallThicknessEntry.bind('<Return>', self.wallThicknessCommand)
        self.wallThicknessEntry.bind('<Tab>', self.wallThicknessCommand)
        self.wallThicknessEntry.grid(row=1, column=3, pady=4)

        tkinter.Label(self.master, text="Number of Holes").grid(row=2, column=0, sticky=tkinter.E, pady=4)
        self.numHolesEntry = tkinter.Entry(self.master, validate="focusout", validatecommand=self.numHolesCommand)
        self.numHolesEntry.bind('<Return>', self.numHolesCommand)
        self.numHolesEntry.bind('<Tab>', self.numHolesCommand)
        self.numHolesEntry.grid(row=2, column=1, pady=4)

        tkinter.Label(self.master, text="Select Bell Note").grid(row=2, column=2, sticky=tkinter.E, pady=4)
        self.bellNoteCombo = ttk.Combobox(self.master, state="readonly", values=self.data_store.bellNoteArray)
        self.bellNoteCombo.config(width=17)
        self.bellNoteCombo.grid(row=2, column=3, pady=4)
        self.bellNoteCombo.bind("<<ComboboxSelected>>", self.bellSelectCallback)

        tkinter.Label(self.master, text="Embouchure Area").grid(row=3, column=0, sticky=tkinter.E, pady=4)
        self.embouchureAreaEntry = tkinter.Entry(self.master)
        self.embouchureAreaEntry.grid(row=3, column=1, pady=4)

        tkinter.Label(self.master, text="Bell Frequency").grid(row=3, column=2, sticky=tkinter.E, pady=4)
        self.bellFreqEntry = tkinter.Entry(self.master)
        self.bellFreqEntry.grid(row=3, column=3, sticky=tkinter.E, pady=4)

        tkinter.Label(self.master, text="Units of Measure").grid(row=4, column=0, sticky=tkinter.E, pady=4)
        self.measureUnitsOpt = ttk.Combobox(self.master, state="readonly", values=["inch", "mm"])
        self.measureUnitsOpt.config(width=17)
        self.measureUnitsOpt.grid(row=4, column=1, pady=4)
        self.measureUnitsOpt.bind("<<ComboboxSelected>>", self.measureUnitsCallback)

        tkinter.Label(self.master, text="Display Format").grid(row=4, column=2, sticky=tkinter.E, pady=4)
        self.displayFormatOpt = ttk.Combobox(self.master, state="readonly", values=["decimal", "fraction"])
        self.displayFormatOpt.current(1)
        self.displayFormatOpt.config(width=17)
        self.displayFormatOpt.grid(row=4, column=3, pady=4)
        self.displayFormatOpt.bind("<<ComboboxSelected>>", self.displayFormatCallback)

        if self.measureUnitsOpt.get() == 'mm':
            self.displayFormatOpt.config(state="readonly")

        self.refreshButton = tkinter.Button(
            self.master, text="Refresh", width=14, command=self.refreshButtonCommand)
        self.refreshButton.grid(row=5, column=0, pady=4)

        self.printButton = tkinter.Button(self.master, text="Print", width=14, command=self.printButtonCommand)
        self.printButton.grid(row=5, column=1, pady=4)

        self.setEmbouchureButton = tkinter.Button(self.master, text="Embouchure", width=14, command=self.setEmbouchureCommand)
        self.setEmbouchureButton.grid(row=5, column=2, pady=4)

        self.setOtherButton = tkinter.Button(self.master, text="Other Parameters", width=14, command=self.setOtherCommand)
        self.setOtherButton.grid(row=5, column=3, pady=4)

        #self.refresh()
        self.set_state() # write what's in the data_store to the GUI

    @debugger
    def get_state(self):
        '''
        Return the state of the controls in the upper half into the data store.
        '''

        if self.displayFormatOpt.current() == 0:
            self.data_store.set_disp_frac(False)
        else:
            self.data_store.set_disp_frac(True)

        if self.measureUnitsOpt.current() == 0:
            self.data_store.set_units(False)
        else:
            self.data_store.set_units(True)

        self.data_store.set_title(self.titleEntry.get())
        self.data_store.set_inside_dia(float(self.insideDiaEntry.get()))
        self.data_store.set_wall_thickness(float(self.wallThicknessEntry.get()))
        self.data_store.set_number_holes(int(self.numHolesEntry.get()))
        self.data_store.set_bell_note_select(self.bellNoteCombo.current())
        self.data_store.set_embouchure_area(float(self.embouchureAreaEntry.get()))
        self.data_store.set_bell_freq(
            self.data_store.note_table[self.data_store.get_bell_note_select()]['frequency'])


    @debugger
    def set_state(self):
        '''
        Take the state from the data store and put in the GUI.
        '''
        self.titleEntry.delete(0, tkinter.END)
        self.titleEntry.insert(0, self.data_store.get_title())

        self.bellNoteCombo.current(self.data_store.get_bell_note_select())
        self.measureUnitsOpt.current(int(self.data_store.get_units())) # it's a bool in the data_store
        self.displayFormatOpt.current(int(self.data_store.get_disp_frac())) # it's a bool in the data_store

        self.insideDiaEntry.delete(0, tkinter.END)
        self.insideDiaEntry.insert(0, str(self.data_store.get_inside_dia()))

        self.wallThicknessEntry.delete(0, tkinter.END)
        self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))

        self.numHolesEntry.delete(0, tkinter.END)
        self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))

        self.bellFreqEntry.config(state=tkinter.NORMAL)
        self.bellFreqEntry.delete(0, tkinter.END)
        self.bellFreqEntry.insert(0, str(self.data_store.get_bell_freq()))
        self.bellFreqEntry.config(state=tkinter.DISABLED)

        self.embouchureAreaEntry.config(state=tkinter.NORMAL)
        self.embouchureAreaEntry.delete(0, tkinter.END)
        self.embouchureAreaEntry.insert(0, str(self.data_store.get_embouchure_area()))
        self.embouchureAreaEntry.config(state=tkinter.DISABLED)


    @debugger
    def insideDiaCommand(self, event=None):
        try:
            v = self.insideDiaEntry.get()
            n = float(v)
            if self.data_store.get_inside_dia() != n:
                self.logger.debug("change wall from %f to %f"%(self.data_store.get_inside_dia(), n))
                self.data_store.set_inside_dia(n)
                self.insideDiaEntry.delete(0, tkinter.END)
                self.insideDiaEntry.insert(0, str(n))
                raise_event("CALCULATE_EVENT")
            else:
                self.logger.debug("ignore")
            return True
        except ValueError:
            messagebox.showerror("Error", "Could not convert inside diameter to a floating point number.\nRead value was \"%s\"." % (v))
            return False
        except IndexError:
            pass # ignore always. happens as a result of tkinter's message handling


    @debugger
    def wallThicknessCommand(self, event=None):
        try:
            v = self.wallThicknessEntry.get()
            n = float(v)
            if n != self.data_store.get_wall_thickness():
                self.logger.debug("change wall from %f to %f"%(self.data_store.get_wall_thickness(), n))
                self.data_store.set_wall_thickness(n)
                self.wallThicknessEntry.delete(0, tkinter.END)
                self.wallThicknessEntry.insert(0, str(n))
                raise_event("CALCULATE_EVENT")
            else:
                self.logger.debug("ignore")
            return True
        except ValueError:
            messagebox.showerror("Error", "Could not convert wall thickness to a floating point number.\nRead value was \"%s\"." % (v))
            return False
        except IndexError:
            pass


    @debugger
    def numHolesCommand(self, event=None):
        n = 0
        try:
            v = self.numHolesEntry.get()
            n = int(v)
            if n >= 1 and n <= 12:
                # only raise the event if the number of holes is different from 
                # what is in the data_store
                if n != self.data_store.get_number_holes():
                    self.logger.debug("change number of holes from %d to %d"%(self.data_store.get_number_holes(), n))
                    self.data_store.set_number_holes(n)
                    raise_event('UPDATE_LOWER_FRAME_EVENT')
                else:
                    self.logger.debug("ignore")
                return True
            else:
                self.numHolesEntry.delete(0, tkinter.END)
                self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))
                messagebox.showerror("Error", message="Number of holes must be an integer between 1 and 12.\nRead value was \"%s\"." % (v))
                return False
        except ValueError as e:
            print(repr(e))
            self.numHolesEntry.delete(0, tkinter.END)
            self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))
            messagebox.showerror("Error", message="Could not convert number of holes to an integer.\nRead value was \"%s\"." % (v))
            return False
        except IndexError:
            self.numHolesEntry.delete(0, tkinter.END)
            self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))


    @debugger
    def displayFormatCallback(self, event):
        #print(self.displayFormatOpt.current(),self.data_store.get_disp_frac())
        if self.displayFormatOpt.current() == 0:
            val = False
        else:
            val = True

        if val != self.data_store.get_disp_frac():
            self.data_store.set_disp_frac(val)
            raise_event("UPDATE_HOLE_EVENT")
            self.logger.debug("current format set to: %s"%(str(self.data_store.get_disp_frac())))
        else:
            self.logger.debug("ignore")


    @debugger
    def measureUnitsCallback(self, event):
        if self.measureUnitsOpt.current() == 0:
            val = False
        else:
            val = True

        if self.data_store.get_units() != val:
            if self.measureUnitsOpt.current() == 0:
                self.displayFormatOpt.config(state=tkinter.DISABLED)
            else:
                self.displayFormatOpt.config(state="readonly")
            self.data_store.set_units(val)
            raise_event("CHANGE_UNITS_EVENT")
            self.logger.debug("current units set to: %s"%(str(self.data_store.get_units())))
        else:
            self.logger.debug("ignore")
        

    @debugger
    def bellSelectCallback(self, event):
        '''
        Change the data_store to match the new bell selection
        '''
        val = self.bellNoteCombo.current()
        if val != self.data_store.get_bell_note_select():
            self.data_store.set_bell_note_select(val)
            self.logger.debug("current bell selection set to: %d"%(self.data_store.get_bell_note_select()))
            raise_event("UPDATE_NOTES_EVENT")
        else:
            self.logger.debug("ignore")


    @debugger
    def refreshButtonCommand(self):
        self.refreshButton.focus_set()
        self.get_state()
        raise_event('UPDATE_LINES_EVENT')


    @debugger
    def setEmbouchureCommand(self):
        self.setEmbouchureButton.focus_set()


    @debugger
    def setOtherCommand(self):
        self.setOtherButton.focus_set()


    @debugger
    def printButtonCommand(self):
        self.printButton.focus_set()
