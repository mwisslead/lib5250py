"""
Session object
Created by Kenneth J. Pouncey 2002-05-19
"""
from vt5250 import vt5250
from Screen5250 import Screen5250

__all__ = ["Session"]

# Tunable parameters
DEBUGLEVEL = 0

class Session:
    """Session interface class."""
    def __init__(self, host=None, port=0):
        """Constructor."""
        self.debuglevel = DEBUGLEVEL
        self.vt = vt5250(host, port)
        self.vt.set_debuglevel(self.debuglevel)
        self.screen = Screen5250()
        self.screen.set_debuglevel(self.debuglevel)
        self.vt.setScreen(self.screen)
        self.screen.setVT(self.vt)

    def set_debuglevel(self, debuglevel):
        """
        Set the debug level.
        The higher it is, the more debug output you get (on sys.stdout).
        """
        self.debuglevel = debuglevel
        self.vt.set_debuglevel(self.debuglevel)
        self.screen.set_debuglevel(self.debuglevel)

    def connect(self):
        self.vt.open()

    def disconnect(self):
        self.vt.close()

    def getScreen(self):
        return self.screen