from tkinter import messagebox
from logger import Logger

class BaseException(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class AppError(BaseException):

    def __init__(self, msg, func):
        super().__init__(msg)
        self.logger = Logger(title, Logger.ERROR)
        self.msg = msg

    def __str__(self):
        return self.msg

    def show(self):
        messagebox.showerror(title="Error", message=func+": "+self.msg)
        self.logger.error(self.msg)

class AppWarning(BaseException):

    def __init__(self, msg, func):
        
        super().__init__(msg)
        self.logger = Logger(title, Logger.WARNING)
        self.msg = msg

    def __str__(self):
        return self.msg

    def show(self):
        messagebox.showerror(title="Warning", message=func+": "+self.msg)
        self.logger.warning(self.msg)

class AppFatalError(BaseException):

    def __init__(self, msg, func):
        
        super().__init__(msg)
        self.logger = Logger(title)
        self.msg = msg

    def __str__(self):
        return self.msg

    def show(self):
        messagebox.showerror(title="Fatal Error", message=func+": "+self.msg)
        self.logger.fatal(self.msg)

