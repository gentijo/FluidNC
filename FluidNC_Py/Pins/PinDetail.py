#// Copyright (c) 2021 -  Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.



#// Implementation details of pins.
class PinDetail:

    def __init__(self, **):
        self._index:int = None
        #PinDetail(int number) : _index(number) {}
        #PinDetail(const PinDetail& o) = delete;
        #PinDetail(PinDetail&& o)      = delete;
        
        
    def set(self, pd:PinDetail) -> PinDetail:
        return None

    def capabilities() -> PinCapabilities:
        return None


    #// I/O:
    def write(self, high:int) -> None:
        pass

    def synchronousWrite(self, high:int) -> None:
        pass

    def read(self) -> int:
        pass

    def setAttr(self, value:PinAttributes) -> None:
        pass
    
    def getAttr(self) -> PinAttributes:
         return None

    def registerEvent(self, obj:EventPin) -> None:
        pass

    def __str__(self) -> str:
        return ""

    def number(self,) -> int: 
        return _index; 

