#// Copyright (c) 2021 -  Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.



class VoidPinDetail(PinDetail):
    def __init__(self, **kwargs):
        if "number" in kwargs:
                pass
        elif "options" in kwargs:
                pass
        pass

    #explicit VoidPinDetail(int number = 0);
    #explicit VoidPinDetail(const PinOptionsParser& options);

    def capabilities(self) -> PinCapabilities:
        #// Void pins support basic functionality. It just won't do you any good.
        return PinCapabilities::Output | PinCapabilities::Input | PinCapabilities::ISR | PinCapabilities::Void;pass

    #// I/O:
    def write(self, high:int) -> None:
        pass

    def read(self) -> int:
        return 0

    def setAttr(self, value:PinAttributes) -> None:
        pass


    def getAttr(self) -> PinAttributes
        return PinAttributes::None;

    def toString(self) -> str:
        return "NO_PIN"
    
    

