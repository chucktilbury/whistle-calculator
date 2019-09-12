from tkinter import messagebox
from logger import Logger

class AppError(Exception):

    def __init__(self, func, msg, excep=None):

        super().__init__(msg)
        self.logger = Logger(func, Logger.ERROR)
        self.msg = msg
        self.func = func
        self.excep = excep

    def __str__(self):
        return self.msg

    def show(self):
        if not self.excep is None:
            self.logger.error(str(self.excep))
        messagebox.showerror(title="Error", message=self.func+": "+self.msg)
        self.logger.error(self.msg)

class AppWarning(Exception):

    def __init__(self, func, msg, excep=None):
        
        super().__init__(msg)
        self.logger = Logger(func, Logger.WARNING)
        self.msg = msg
        self.func = func
        self.excep = excep

    def __str__(self):
        return self.msg

    def show(self):
        if not self.excep is None:
            self.logger.error(str(self.excep))
        messagebox.showerror(title="Warning", message=self.func+": "+self.msg)
        self.logger.warning(self.msg)

class AppFatalError(Exception):

    def __init__(self, func, msg, excep=None):
        
        super().__init__(msg)
        self.logger = Logger(func)
        self.msg = msg
        self.func = func
        self.excep = excep

    def __str__(self):
        return self.msg

    def show(self):
        if not self.excep is None:
            self.logger.error(str(self.excep))
        messagebox.showerror(title="Fatal Error", message=self.func+": "+self.msg)
        self.logger.fatal(self.msg) # exit the program

