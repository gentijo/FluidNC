#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import Configurable

from HandlerBase import HandlerBase, HandlerType, speedEntry
from UartTypes import UartData, UartParity, UartStop


class GCodeParam( HandlerBase ):

    #GCodeParam(const char* key, float& iovalue, bool get);
    #std::string setting_prefix();

    def __init__(self):
        self.setting:str = ""
        self.start:str = ""
        self._get:bool = False
        self_iovalue:float = None
        self.isHandled:bool = False;


    def _is(self,name:str) -> bool:
        if self.start:
            len = len(name)
            result:bool = None # !strncasecmp(name, start_, len) && (start_[len] == '\0' || start_[len] == '/');
            return result
        else:
            return False


    def error(self) -> None:
        assert(False, "Non-numeric config item")


    def enterSection(self, name:str, value:Configurable) -> None:
        if (is(name) && !isHandled_) {
            previous = self.start_;

            #// Figure out next node
            next = start_;
            for (; *next && *next != '/'; ++next) {}

            // Do we have a child?
            if (*next == '/' && next[1] != '\0') {
                ++next;
                start_ = next;
                // Handle child:
                value->group(*this);
            } else {
                error();
            }

            #// Restore situation:
            start_ = previous;


    def matchesUninitialized(self, name:str) -> bool:
        return False


    def item(self, name:str, value:bool) -> None:
        if (is(name)) {
            isHandled_ = true;
            if (_get) {
                _iovalue = value;
            } else {
                value = _iovalue;
            }
        }
    }

    def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
        if isName(name):
            isHandled_ = true;
            if self._get():
                self._iovalue = value
            else:
                value = self._iovalue

    #def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
    #    pass 
        # if (is(name)) {
        #     isHandled_ = true;
        #     if (_get) {
        #         _iovalue = value;
        #     } else {
        #         if (_iovalue < 0) {  // constrain negative values to 0
        #             error();
        #         } else {
        #             value = _iovalue;
        #         }
        #        constrain_with_message(value, minValue, maxValue);

    def item(self, name:str, value:float, minValue:float, maxValue:float) -> None:
        if (self.isName(name)):
            self.isHandled_ = true;
            if self._get:
                self._iovalue = value;
            else:
                value = self._iovalue;
                #constrain_with_message(value, minValue, maxValue);

    def item(self, name:str, value:list[speedEntry]) -> None:
        if isName(name):
            self.error();

    def item(self, name:str, value:list[float]) -> None:
        if isName(name):
            error();
        

    def item(self, name:str, wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        pass

    def item(self, name:str, value:str, minLength:int, maxLength:int) -> None:
        if (self.isName(name)) 
            self.error()

    def item(self, name:str, value:Pin) -> None:
       if self.isName(name):
            self.error();
        
    def item(self, name:str, value:IPAddress) -> None:
       if self.isName(name):
            self.error();
        

    def item(self, name:str, value:int, e:EnumItem) -> None:
        if self.isName(name)):
            isHandled_ = True;
            if self._get
                self._iovalue = value;
            else:
                value = self._iovalue;



    def item(self, name:str, value:Macro) -> None:
       if self.isName(name):
            self.error();
    

    def handlerType(self) -> HandlerType  
        return HandlerType.Runtime
