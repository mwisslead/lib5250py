"""
ScreenFields object
Created by Kenneth J. Pouncey 2002-05-23
"""

import ScreenField

__all__ = ["SessionFields"]

# Tunable parameters
CMD_READ_INPUT_FIELDS = 0x42  # 66
CMD_READ_MDT_FIELDS = 0x52  # 82
CMD_READ_MDT_IMMEDIATE_ALT = 0x83  # 131


class ScreenFields:
    """SessionFields interface class."""

    def __init__(self, screen):
        """Constructor."""
        self.screen = screen
        self.clearFFT()

    def clearFFT(self):
        """
            clear field format table
        """
        self.screenFields = []
        self.currentField = None
        self.fieldIds = 0
        self.cpfExists = 0  # clear the cursor progression fields flag
        self.masterMDT = 0

    def existsAtPos(self, pos):
        """
            does a field exist at the position passed in
        """
        return int(any(sf.startPos() == pos for sf in self))

    def isMasterMDT(self):
        """ Is the master modified data tag set """
        return self.masterMDT

    def setCurrentField(self, field):
        """ Set the current field to the field passed in """
        self.currentField = field

    def isCurrentFieldBypassField(self):
        """
        Return whether or not the current field is a bypass field or not
        """
        self.currentField.isBypassField()

    def isCurrentField(self):
        """ Do we have a current field set """
        return self.currentField == None

    def getCurrentField(self):
        """
        return the current field position within the field plane
        """
        return self.currentField

    def setField(self, attr, row, col, len, ffw1, ffw2, fcw1, fcw2):
        """
            Set a field in the current session screen 
        """
        sf = ScreenField.ScreenField(self.screen)
        self.screenFields.append(sf)
        sf.setField(attr, row - 1, col - 1, len, ffw1, ffw2, fcw1, fcw2)
        if not sf.isBypassField():
            self.fieldIds += 1
            sf.setFieldId(self.fieldIds)
        if fcw1 == 0x88:
            self.cpfExists = 1
        if self.currentField != None:
            self.currentField.next = sf
            sf.prev = self.currentField
        self.currentField = sf
        self.masterMDT = self.currentField.mdt
        return self.currentField

    def readFormatTable(self, boasp, readType, codePage):
        """
            Read the current screen fields and format them so that they can
            be sent to the Host
        """
        isSigned = 0
        sb = None
        if self.isMasterMDT:
            for sf in self.screenFields:
                if sf.mdt or (readType == CMD_READ_INPUT_FIELDS):
                    sb = sf.getText()
                    if readType == CMD_READ_MDT_FIELDS or \
                            readType == CMD_READ_MDT_IMMEDIATE_ALT:
                        len2 = len(sb) - 1
                        while len2 >= 0 and sb[len2] < ' ':
                            sb = sb[:-1]
                            len2 -= 1
                    if sf.isSignedNumeric() and len(sb) > 0 and sb[-1] == '-':
                        isSigned = 1
                    len3 = len(sb)
                    if len3 > 0 or (readType == CMD_READ_MDT_FIELDS or
                                    readType == CMD_READ_MDT_IMMEDIATE_ALT):
                        if len3 > 0 or (readType == CMD_READ_MDT_FIELDS or
                                        readType == CMD_READ_MDT_IMMEDIATE_ALT):
                            boasp.append(17)
                            boasp.append(sf.startRow() + 1)
                            boasp.append(sf.startCol() + 1)
                        k = 0
                        while k < len3:
                            if sb[k] < ' ':
                                boasp.append(codePage.uni2ebcdic(' '))
                            else:
                                if isSigned and k == len3 - 1:
                                    boasp.append(0xd0 | (0x0f & c))
                                else:
                                    boasp.append(
                                        ord(codePage.uni2ebcdic(sb[k])))
                            k += 1

    def __getitem__(self, i):
        return self.screenFields[i]

    def getItem(self, i):
        return self[i]

    def __iter__(self):
        return iter(self.screenFields)

    def __len__(self):
        return len(self.screenFields)

    def getCount(self):
        """ Return the number of fields in the current field plane """
        return len(self)

    def isInField(self, pos, chgToField):
        for sf in self.screenFields:
            if sf.withinField(pos):
                if chgToField:
                    self.currentField = sf
                return 1
        return 0