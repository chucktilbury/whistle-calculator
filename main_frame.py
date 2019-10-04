from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter
import sys, os

from data_store import DataStore
from calculate import Calculator
from lower_frame import LowerFrame
from upper_frame import UpperFrame
from utility import Logger, debugger, raise_event
from exception import AppFatalError
#from configuration import Configuration
import utility 
import dialogs

class MainFrame(tkinter.Frame):
    '''
    This is the main frame that "contains" the other frames.
    '''
    def __init__(self, master=None):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)

        tkinter.Frame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        self.general_params = tkinter.LabelFrame(self.master, text="General Parameters")
        self.general_params.pack()
        self.output_params = tkinter.LabelFrame(self.master, text="Output Parameters")
        self.output_params.pack(fill="both", expand="yes")

        # set up some default values
        self.current_file_name = os.path.join(os.getcwd(), "untitled.wis")
        
        self.data = DataStore.get_instance()
        self.logger.debug("data store: %s"%(str(self.data)))

        self.calc = Calculator()
        self.upper_frame = UpperFrame(self.general_params)
        self.lower_frame = LowerFrame(self.output_params)

        menu = tkinter.Menu(self.master, tearoff=0)
        self.master.config(menu=menu)
        #self.master.geometry("750x450")

        fileMenu = tkinter.Menu(menu, tearoff=0)
        fileMenu.add_command(label="Load", command=self.loadCommand)
        fileMenu.add_command(label="Save", command=self.saveCommand)
        fileMenu.add_command(label="Save As", command=self.saveasCommand)
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=self.close_window)
        menu.add_cascade(label="File", menu=fileMenu)

        editMenu = tkinter.Menu(menu, tearoff=0)
        editMenu.add_command(label="Help", command=self.helpCommand)
        editMenu.add_command(label="About", command=self.aboutCommand)
        editMenu.add_command(label="Dump", command=self.dumpInternalData)
        menu.add_cascade(label="Help", menu=editMenu)

        tkinter.Label(self.master, text="Tilbury Woodwinds Whistle Calculator",
                    font=("Helvetica", 14)).pack()

        self.upper_frame.create_frame()
        self.lower_frame.update_frame()

    @debugger
    def set_state(self):
        self.upper_frame.set_state()
        self.lower_frame.set_state()

    @debugger
    def get_state(self):
        self.upper_frame.get_state()
        self.lower_frame.get_state()

    @debugger
    def close_window(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.logger.debug('quit')
            self.master.destroy()
        else:
            self.logger.debug('ignore')

    @debugger
    def loadCommand(self):
        f = filedialog.askopenfilename(initialfile=self.current_file_name, filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
        if f != '':
            self.logger.debug("loading file: %s"%(f))
            self.data.load(f)
            self.data.set_file_name(f)
            raise_event("UPDATE_LOWER_FRAME_EVENT")
            self.set_state()
        else:
            self.logger.debug("cancel")

    @debugger
    def saveCommand(self):
        d = filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True)
        p = os.path.join(d, self.data.get_file_name())
        if p != '':
            print("saving file = " + p )
            self.data.save(p)
        else:
            self.logger.debug("cancel")

    @debugger
    def saveasCommand(self):
        f = filedialog.asksaveasfilename(initialfile=self.current_file_name, filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
        if f != '':
            print("file save as = " + f)
            self.data.save(f)
            self.data.set_file_name(f)
        else:
            self.logger.debug("cancel")

    @debugger
    def aboutCommand(self):
        messagebox.showinfo(
            "About", "Tilbury Woodwinds Company\nWhistle Calculator\nChuck Tilbury (c) 2019")

    @debugger
    def dumpInternalData(self):
        self.data.print_data()
        utility.dump_events()

    @debugger
    def helpCommand(self):
        #messagebox.showinfo(
        #    "Help", 
        dialogs.helpDialog(self.master)
