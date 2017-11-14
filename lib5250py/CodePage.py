"""
CodePage
Used to convert ascii to ebcdic and ebcdic to ascii
Created by Kenneth J. Pouncey 2002-05-18
Changed by Nate Custer - 2002-05-22
    Used some different data types to improve performance/memory usage.
    Used a dict (hash table) instead of a list for the lookup tables.
    The performance of a lookup is faster if you use a dict. Also; used a
    tuple instead of a list for the list at the start. Since tuples aren't
    mutable the python interpreter uses less memory to store them.
Cleaned up by P. Bielen - 2002-05-23
    Managed a length of 75 characters at one line, to prevend a lot of
    editors to do a word-wrap.
"""

__all__ = ["CodePage"]


class CodePage:

    def __init__(self, codePage=None):
        self.setCodePage(codePage)

    def setCodePage(self, codePage):
        codec = {
            37: 'IBM037',
        }.get(codePage, 'IBM037')

        rawbytes = bytes(bytearray(list(range(256))))
        rawunicode = rawbytes.decode('latin-1')

        self.ebcdic = tuple(ord(x) for x in rawbytes.decode(codec))
        self.ascii = tuple(x for x in bytearray(rawunicode.encode(codec)))

    def getEBCDIC(self, index):
        return self.ascii[index]

    def getEBCDICChar(self, index):
        return chr(self.ascii[index])

    def getASCII(self, index):
        return self.ebcdic[index]

    def getASCIIChar(self, index):
        return chr(self.ebcdic[index])

    def ebcdic2uni(self, index):
        return self.getASCIIChar(index)

    def uni2ebcdic(self, index):
        return self.getEBCDICChar(ord(index))
