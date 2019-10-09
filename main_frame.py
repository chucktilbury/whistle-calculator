from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter
import sys, os, time

from data_store import DataStore
from calculate import Calculator
from lower_frame import LowerFrame
from upper_frame import UpperFrame
from utility import Logger, debugger, raise_event
#from exception import AppFatalError
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
        #self.current_file_name = os.path.join(os.getcwd(), "untitled.wis")
        
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
        fileMenu.add_command(label="Export", command=self.exportCommand)
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=self.close_window)
        menu.add_cascade(label="File", menu=fileMenu)

        settingsMenu = tkinter.Menu(menu, tearoff=0)
        settingsMenu.add_command(label="Constants", command=self.constCommand)
        settingsMenu.add_command(label="Embouchure", command=self.emboCommand)
        settingsMenu.add_command(label="Notes", command=self.notesCommand)
        menu.add_cascade(label="Settings", menu=settingsMenu)

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
        if self.data.get_change_flag():
            if messagebox.askyesno("Quit", "Do you want to save the changes before quitting?"):
                self.logger.debug('save')
                self.saveCommand()
            else:
                self.logger.debug('ignore')
        self.master.destroy()

    @debugger
    def loadCommand(self):
        f = filedialog.askopenfilename(initialfile=self.data.get_file_name(), filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
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
        #d = filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True)
        #p = os.path.join(d, self.data.get_file_name())
        p = os.path.join(os.getcwd(), self.data.get_file_name())
        if p != '':
            self.logger.debug("saving file = " + p )
            self.data.save(p)
        else:
            self.logger.debug("cancel")

    @debugger
    def saveasCommand(self):
        f = filedialog.asksaveasfilename(initialfile=self.data.get_file_name(), filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
        if f != '':
            self.logger.debug("file save as = " + f)
            self.data.save(f)
            self.data.set_file_name(f)
        else:
            self.logger.debug("cancel")

    @debugger
    def aboutCommand(self):
        messagebox.showinfo(
            "About", "Tilbury Woodwinds Company\nWhistle Calculator\nChuck Tilbury (c) 2019\nVersion: 1.0\nData Version: %s"%(self.data.get_version()))

    @debugger
    def dumpInternalData(self):
        self.data.print_data()
        utility.dump_events()

    @debugger
    def helpCommand(self):
        #messagebox.showinfo(
        #    "Help", 
        dialogs.helpDialog(self.master)

    @debugger
    def exportCommand(self):
        name = self.data.get_file_name().replace('.wis', '.txt')
        f = filedialog.asksaveasfilename(initialfile=name, filetypes=(("Text Files","*.txt"), ("all files", "*.*")))
        if f != '':
            self.logger.debug("export file as = " + f)
            with open(f, 'w') as fh:
                fh.write("\n%s\n"%("-"*60))
                fh.write("%s\n"%(self.data.get_title()))
                fh.write("%s\n\n"%("-"*60))
                fh.write("BELL:       %s (%0.3f Hz)\n"%(
                            self.data.note_table[self.data.get_bell_note_select()]['note'], 
                            self.data.note_table[self.data.get_bell_note_select()]['frequency']))
                fh.write("ID:         %0.3f\n"%(self.data.get_inside_dia()))
                fh.write("WALL:       %0.3f\n"%(self.data.get_wall_thickness()))
                fh.write("NUM HOLES:  %d\n"%(self.data.get_number_holes()))
                if self.data.get_units() == False:
                    fh.write("UNITS:      inches\n")
                else:
                    fh.write("UNITS:      millimeters\n")
                fh.write("LENGTH:     %0.4f\n"%(self.data.get_length()))
                fh.write("\n%s\n"%("-"*60))
                fh.write("          Drill     Location    Note       Frequency\n")
                for x in range(self.data.get_number_holes()):
                    fh.write("%-10s"%("Hole %d"%(x+1)))

                    if not self.data.get_units():
                        if self.data.get_disp_frac():
                            fh.write("%-10s"%(utility.reduce(self.data.get_hole_size(x))))
                        else:
                            fh.write("%-10s"%("%0.4f"%(self.data.get_hole_size(x))))
                    else:
                        fh.write("%-10s"%("%0.4f"%(self.data.get_hole_size(x))))

                    fh.write("%-12s"%("%0.4f"%(self.data.get_hole_xloc(x))))
                    fh.write("%-10s "%(self.data.get_hole_note(x)))
                    fh.write("%0.4f Hz\n"%(self.data.get_hole_freq(x)))

                fh.write("\n%s\n"%("-"*60))
                fh.write("Notes:\n\n")
                fh.write("%s"%(self.data.get_notes()))
                fh.write("\n%s\n"%("-"*60))
                fh.write("\nCut sheet generated on %s\nby Tilbury Woodwinds Whistle Calculator\n\n"%(time.ctime()))

        else:
            self.logger.debug("cancel")

    @debugger
    def emboCommand(self):
        dialogs.EmbouchureDialog(self.master)
        raise_event("UPDATE_LOWER_FRAME_EVENT")
        raise_event("UPDATE_UPPER_EVENT")

    @debugger
    def constCommand(self):
        dialogs.ConstDialog(self.master)
        raise_event("UPDATE_LOWER_FRAME_EVENT")
        raise_event("UPDATE_UPPER_EVENT")

    @debugger
    def notesCommand(self):
        dialogs.NotesDialog(self.master)

    #@debugger
    #def printButtonCommand(self):
    #    self.printButton.focus_set()
