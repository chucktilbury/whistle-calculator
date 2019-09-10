import time
import sys

class Logger(object):

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    MESSAGE = 4
    STDERR = 0
    STDOUT = 1

    def __init__(self, name, level=DEBUG, stream=STDOUT):

        self.dbg = 0
        self.inf = 1
        self.warn = 2
        self.err = 3
        self.mess = 4
        self.stderr = 0
        self.stdout = 1

        self.name = name 
        self.level = []
        self.level.insert(0, level)

        if stream == self.STDERR:
            self.stream = sys.stderr
        else:
            self.stream = sys.stdout

    def fmt(self, args, lev):
        t = time.strftime("(%Y%m%d %H:%M:%S)")
        return "%s %s: %s: %s\n"%(t, self.name, lev, args)

    def debug(self, args):
        if self.level[0] <= self.dbg:
            self.stream.write(self.fmt(args, 'DEBUG'))

    def info(self, args):
        if self.level[0] <= self.inf:
            self.stream.write(self.fmt(args, 'INFO'))

    def warning(self, args):
        if self.level[0] <= self.warn:
            self.stream.write(self.fmt(args, 'WARNING'))

    def error(self, args):
        if self.level[0] <= self.err:
            self.stream.write(self.fmt(args, 'ERROR'))

    def msg(self, args):
        if self.level[0] <= self.mess:
            self.stream.write(self.fmt(args, 'MSG'))

    def fatal(self, args):
        self.stream.write(self.fmt(args, 'FATAL ERROR'))
        self.stream.write("System cannot continue\n\n")
        sys.exit(1)

    def push_level(self, level):
        self.level.insert(0, level)

    def pop_level(self):
        if len(self.level) > 1:
            self.level.remove(0)

    def set_level(self, level):
        self.level[0] = level