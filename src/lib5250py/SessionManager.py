"""
SessionManager and Sessions objects
Created by Nathanael Custer 2002-07-01
"""

from Sessions import Sessions

__all__ = ["SessionManager"]

# Tunable parameters
DEBUGLEVEL = 0

# Telnet Port
TELNET_PORT = 23

class SessionManager:
    def __init__(self):
        self.MasterSessionList = Sessions()
    def getSessions(self):
        return self.MasterSessionList
    def openSession(self, name=''):
        self.MasterSessionList._addSession(name)
        return self.MasterSessionList.item(name)
    def closeSession(self, name=''):
        session = self.MasterSessionList.item(name)
        if session.isConected():
            session.disconect()
        self.MasterSessionList._delSession(name)
    def refresh(self):
        return self.MasterSessionList
