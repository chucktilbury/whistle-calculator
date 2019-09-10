from tkinter import ttk
from tkinter import messagebox
import tkinter
import sys, os

from data_store import DataStore
from calc import Calculator
from lower_frame import LowerFrame
from upper_frame import UpperFrame
from logger import Logger
from exception import AppFatalError

class MainFrame(tkinter.Frame):
    '''
    This is the main frame that "contains" the other frames.
    '''
    def __init__(self, master=None):
        self.logging = Logger("MainFrame")
        self.logging.debug("constructor")

        tkinter.Frame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        self.general_params = tkinter.LabelFrame(self.master, text="General Parameters")
        self.general_params.pack()
        self.output_params = tkinter.LabelFrame(self.master, text="Output Parameters")
        self.output_params.pack(fill="both", expand="yes")

        # set up some default values
        self.current_file_name = os.path.join(os.getcwd(), "untitled.wis")
        self.data = DataStore()
        self.calc = Calculator(self.data)
        self.upper_frame = UpperFrame(self.general_params, self.data)
        self.lower_frame = LowerFrame(self.output_params, self.data)

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
        menu.add_cascade(label="Help", menu=editMenu)

        tkinter.Label(self.master, text="Tilbury Woodwinds Whistle Calculator",
                    font=("Helvetica", 14)).pack()

        self.upper_frame.create_frame()
        self.lower_frame.create_frame()

    def close_window(self):
        self.logging.debug("close_window")
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.master.destroy()

    def loadCommand(self):
        self.logging.debug("loadCommand")
        f = tkinter.filedialog.askopenfilename(initialfile=self.current_file_name, filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
        print("loading file = " + f)

    def saveCommand(self):
        self.logging.debug("saveCommand")
        d = tkinter.filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True)
        p = os.path.join(d, self.current_file_name)
        print("saving file = " + p )
        #f = open(p, 'w')
        #f.close()

    def saveasCommand(self):
        self.logging.debug("saveasCommand")
        f = tkinter.filedialog.asksaveasfilename(initialfile=self.current_file_name, filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
        print("file save as = " + f)

    def helpCommand(self):
        self.logging.debug("helpCommand")
        #print("display format: "+ self.displayFormatOpt.get())
        #print("measure units: "+ self.measureUnitsOpt.get())
        #print("bellnote: %s (%d)"%(str(self.bellNoteEntry.get()), self.bellNoteEntry.current()))

    def aboutCommand(self):
        self.logging.debug("aboutCommand")
        messagebox.showinfo(
            "About", "Tilbury Woodwinds Company\nWhistle Calculator\nChuck Tilbury (c) 2019")
