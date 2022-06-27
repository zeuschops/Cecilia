from datetime import datetime
from io import TextIOWrapper
import os

"""
Debugging severity levels documentation:
- 0, used for debugging
- 1, informational generic process-level diagnostics
- 2, used for invalid endpoints (ex. invalid SQLite table key called)
- 3, used for invalid response resources (ex. invalid API Keys, invalid endpoint URL)
- 4, used for errors (ex. port already used and failing over to next available port during startup, another instance determined to be running, or something nearly application-breaking but known may be caught in here)
"""

#Debuggers should be singleton objects as the content being written to disk can only have one resource accessing them at a time
class Debugger:
    def __init__(self, filename:str="../Logs/log-%s.txt" % (datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), log_level:int=0, debugging_mode:bool=False):
        self.filename = filename
        if 'Logs' not in os.listdir('../'):
            os.mkdir('../Logs')
        self.log_level = log_level
        self.log_file = open(self.filename, 'w')
        self.debugging_mode = debugging_mode
    
    #Singleton verification stuff
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Debugger, cls).__new__(cls)
        return cls.instance
    
    def log(self, severity:int, content:str):
        if not self.debugging_mode:
            if severity > 0:
                self.log_file.write('%i | %s' % (severity, content))
        else:
            self.log_file.write('%i | %s' % (severity, content))
    
    def new_logger(self, use_existing_logfile:bool) -> TextIOWrapper:
        if use_existing_logfile:
            self.log_file.close()
            self.filename = "log-%s.txt" % datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self.log_file = open(self.filename, 'w')
            return None
        else:
            self.filename_2 = "log-%s.txt" % datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self.log_file = open(self.filename, 'w')
            return self.log_file
