import Session
import Screen5250
import ScreenFields
import CodePage
from sys import argv

__all__ = ["testsession"]

myScreen = None

class testsession:

    def __init__(self):
        self.first = 1
        self.USERID = None
        self.PASSWORD = None
                
    def outputScreen(self,initiator,startRow,startColumn,endRow,endColumn):
        """
        Callable method to get screen updates
        """
        print 'ScreenUpdated - initiated from ',initiator, \
              ' Starting from -> ',startRow,endRow,' to -> ',endRow,endColumn

        if initiator == 0:  ## 0  is from client and 1 is from host
            return
        
        # Note we only print the first 12 rows here
        indices = range(1,24)
    #    for idx in indices:
    #        print myScreen.getPlaneData(idx,1,idx,80,1)
    #        print self.screen.getPlaneData(idx,1,80,2)

        fields = myScreen.getFields()

        if self.USERID == None or self.PASSWORD == None:
            self.USERID = raw_input("What's your username ? > ")
            self.PASSWORD = raw_input("What's your password ? > ")
        
        if self.first == 1:
            field = fields.getItem(0)
            field.setString(self.USERID)
            field = fields.getItem(1)
            field.setString(self.PASSWORD)
        
        for field in fields:
    #        print field.toString()
            print field.getText()
            
    #    print fields.readFormatTable(0x42,CodePage.CodePage())
    #    print myScreen.getFields().readFormatTable(0x52,CodePage.CodePage())
        # Note we only print the first 12 rows here
        indices = range(1,25)
        for idx in indices:
            print myScreen.getPlaneData(idx,1,idx,80,1)
        
        print 'number of fields',myScreen.getFields().getCount()

        if self.first < 7:
            myScreen.sendAidKey(0xF1)
            self.first += 1

    
if __name__ == '__main__':


    if len(argv) >= 2: host = argv[1]
    else:
        host = raw_input('Enter the name of the AS/400-machine > ')


    ts = testsession()
    if len(argv) > 3:
        ts.USERID = argv[2]
        ts.PASSWORD = argv[3]
    session = Session.Session(host)
    session.set_debuglevel(1)
    myScreen = session.getScreen()
    session.getScreen().add_screen_listener(ts.outputScreen)
    session.connect()
    
