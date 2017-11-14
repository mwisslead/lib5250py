"""
Session object
Created by Kenneth J. Pouncey 2002-05-19
"""
from vt5250 import vt5250
from Screen5250 import Screen5250

__all__ = ["Session"]


class Session:
    """Session interface class."""

    def __init__(self, host=None, port=0):
        """Constructor."""
        self.vt = vt5250(host, port)
        self.screen = Screen5250()
        self.vt.setScreen(self.screen)
        self.screen.setVT(self.vt)

    def connect(self):
        self.vt.open()

    def disconnect(self):
        self.vt.close()

    def getScreen(self):
        return self.screen