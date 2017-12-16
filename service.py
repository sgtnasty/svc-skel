#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Ronaldo Nascimento"
__copyright__ = "Copyright 2017, Ronaldo Nascimento"
__credits__ = ["Ronaldo Nascimento"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Ronaldo Nascimento"
__email__ = "sgtnasty@gmail.com"
__status__ = "Development"


import os
import sys
import logging
import time
import datetime
import argparse
import subprocess
import json
import signal

class Service(object):
    """
    """
    def __init__(self, n, d, v, c, l):
        self.name = n
        self.descr = d
        self.version = v
        self.configfile = c
        self.logfile = l
        self.log = None
        self.args = None
        self.config = None

    def cfg_args(self):
        """
        Parse the command line arguments
        """
        self.parser = argparse.ArgumentParser(
            description=self.descr,
            epilog=("Service Class Version %s" % __version__))
        self.parser.add_argument('--config', 
            metavar='CONFIGFILE', required=False, help='path to config file', 
            default=self.configfile)
        self.parser.add_argument('--logfile',
            metavar='LOGFILE', required=False, help='path to log file',
            default=self.logfile)
        self.parser.add_argument('--version', action='version', 
            version=('%(prog)s ' + self.version))
        self.parser.add_argument('--debug', required=False, 
            help='Enable debugging of this script',
            action="store_true")

    def cfg_log(self):
        """
        Setup logging to stdout/stderr - warning only
        and log file
        """
        self.log = logging.getLogger(self.name)
        self.logform = logging.Formatter('%(asctime)s - %(name)s:%(process)d - %(levelname)s - %(message)s')
        self.log_ch = logging.StreamHandler()
        self.log_ch.setLevel(logging.WARN)
        self.log_ch.setFormatter(self.logform)
        self.log.addHandler(self.log_ch)
        if (self.args == None):
            self.log('arguments not parsed, no log file will be used')
            return
        # try to open the log file passed (may need root privs)
        try:
            self.log_fh = logging.handlers.WatchedFileHandler(self.args.log)

            self.log_fh.setLevel(logging.DEBUG)
            self.log_fh.setFormatter(self.logform)
            self.log.addHandler(self.log_fh)
        except:
            t,v,b = sys.exc_info()
            self.log.error('{}: {}'.format(t,v))

    def cfg_load(self):
        """
        Read the config file from JSON
        """
        try:
            fh = open(self.args.config)
            self.config = json.load(fh)
            fh.close()
        except:
            self.log.error('Error reading config file. %s: %s\n%s' % (sys.exc_type, sys.exc_value, sys.exc_traceback))
            sys.exit(1)

    def prep(self):
        self.cfg_args()

    def configure(self):
        if (self.parser == None):
            if (self.log != None):
                self.log.error('Service class not configured')
            else:
                print('Service class not configured')
            sys.exit(1)
        try:
            self.args = self.parser.parse_args()
            self.cfg_log()
            self.cfg_load()
        except:
            t,v,b = sys.exc_info()
            self.log.error('{}: {}'.format(t,v))
            sys.exit(1)