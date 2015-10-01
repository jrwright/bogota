"""
Wrapper for configuration options.
"""
import os
import ConfigParser

dirname=os.path.dirname(__file__)
if len(dirname) == 0:
    dirname = "."
config = ConfigParser.ConfigParser()
config.read(["%s/defaults.cfg" % dirname, os.path.expanduser('~/.bogotarc')])

class SectionWrapper(object):
    def __init__(self, section):
        self.section = section
    def __getattr__(self, name):
        if config.has_option(self.section, name):
            if self.section=='db' and name=='port':
                return config.getint(self.section, name)
            else:
                return config.get(self.section, name)
        return None

db = SectionWrapper('db')
app = SectionWrapper('app')
