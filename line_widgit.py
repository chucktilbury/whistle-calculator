from tkinter import messagebox
import tkinter

from hole_widgit import HoleSizeWidgit
from logger import Logger

class LineWidgit(tkinter.Frame):
    '''
    This is the GUI widget that represents a single line in the output
    data. It uses the data_store to communicate values into and out of
    itself.
    '''

    def __init__(self,
                    parent,
                    data_store,
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
        self.logger = Logger("LineWidgit", level=Logger.ERROR)
        self.logger.debug("constructor")

        tkinter.Frame.__init__(self, parent)

        self.data_store = data_store
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

        self.hole_ctl = HoleSizeWidgit(self)
        self.hole_ctl.config(padx=25)
        # TODO: make defaults configurable and move to data_store
        self.hole_ctl.set_startval(11/32)
        self.hole_ctl.set_incval(1/64)
        self.hole_ctl.set_maxval(1/2)
        self.hole_ctl.set_minval(3/32)
        self.hole_ctl.set_frac(True)
        #
        self.hole_ctl.grid(row=lineno+1, column=4)

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

    def refresh(self):
        '''
        Place the data in the data_store into the display.
        '''
        self.logger.debug("refresh()")
        data = self.data_store.get_line(self.index)
        self.inter_ctl.delete(0, tkinter.END)
        self.inter_ctl.insert(0, str(data['interval']))
        self.note_ctl_txt.set(str(data['note'])) # Label
        self.freq_ctl_txt.set("%s Hz"%(str(data['freq'])))
        self.locat_ctl_txt.set(str(data['location'])) # Label
        self.diff_ctl_txt.set(str(data['diff'])) # Label
        self.cutoff_ctl_txt.set(str(data['cutoff'])) # Label

        self.hole_ctl.set_units(self.data_store.get_units())
        self.hole_ctl.set_frac(self.data_store.get_disp_frac())

        #self.hole_ctl.set_startval(data['hole']) # HoleWidgit
        self.hole_ctl.set_state(data['hole']) # HoleWidgit

    def store(self, data):
        '''
        Get the data out of the display and place it in the data_store.
        '''
        self.logger.debug("store()")
        data = self.data_store.get_line(self.index)
        data['interval'] = int(self.inter_ctl.get())
        data['note'] = self.note_ctl_txt.get()
        data['freq'] = float(self.freq_ctl_txt.get().split()[0])
        data['hole'] = float(self.hole_ctl.get_state())
        data['location'] = float(self.locat_ctl_txt.get())
        data['diff'] = float(self.diff_ctl_txt.get())
        data['cutoff'] = float(self.cutoff_ctl_txt.get())
        self.data_store.set_line(self.index, data)


    """
    def get_data(self):
        # read the controls into the local vars and return the data structure
        # that the calc section operates upon.
        #print("get_data")
        #print("line.get_data")
        try:
            self.inter = int(self.inter_ctl.get()) # Entry, int
            self.hole = float(self.hole_ctl.get()) # HoleWidgit
            self.note = self.note_ctl_txt.get() # Label, string
            s = self.freq_ctl_txt.get().split() # in the format of "nnn.nnn Hz"
            self.freq = float(s[0]) # Label
            self.locat = float(self.locat_ctl_txt.get()) # Label
            self.diff = float(self.diff_ctl_txt.get()) # Label
            self.cutoff = float(self.cutoff_ctl_txt.get()) # Label

            #print("line.get_data end")
            return {"interval":self.inter,
                    "note":self.note,
                    "freq":self.freq,
                    "hole":self.hole,
                    "location":self.locat,
                    "diff":self.diff,
                    "cutoff":self.cutoff,
                    "units":self.units,
                    "fracs":self.fracs}
        except Exception as e:
            print(repr(e))
            messagebox.showerror("Error", "Failed to convert value in get_data()")
            return None

    def set_data(self):
        #'name':'', 'interval':0, 'note':'', 'freq':0.0, 'hole':0.0, 'location':0.0, 'diff':0.0, 'cutoff':0.0
        self.inter_ctl.delete(0, tkinter.END)
        self.inter_ctl.insert(0, str(self.data_store.get_in))
        self.note_ctl_txt.set(str(self.note)) # Label
        self.freq_ctl_txt.set("%s Hz"%(str(self.freq)))
        self.hole_ctl.set_startval(self.hole) # HoleWidgit
        self.hole_ctl.set_units(self.units)
        self.hole_ctl.set_frac(self.fracs)
        self.locat_ctl_txt.set(str(self.locat)) # Label
        self.diff_ctl_txt.set(str(self.diff)) # Label
        self.cutoff_ctl_txt.set(str(self.cutoff)) # Label


    def store(self, data):
        '''
        Set the internal state of the widget, but do not update the screen.
        '''
        self.inter = data['interval']
        self.note = data['note']
        self.freq = data['freq']
        self.hole = data['hole']
        self.locat = data['location']
        self.diff = data['diff']
        self.cutoff = data['cutoff']
        self.units = data['units'] # True if using mm
        self.fracs = data['fracs']

    def refresh(self):
        pass

    def set_units(self, units):
        if type(units) != type(True):
            messagebox.showerror("Internal Error", "Invalid unit type passed to line class.")
        else:
            self.units = units

    def set_fracs(self, units):
        if type(units) != type(True):
            messagebox.showerror("Internal Error", "Invalid fracs type passed to line class.")
        else:
            self.fracs = units
    """