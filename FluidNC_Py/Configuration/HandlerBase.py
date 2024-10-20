#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import sys

import Configurable
import HandlerType
from UartTypes import UartData, UartParity, UartStop

class speedEntry():
        
    def __init__(self):
        self.speed:SpindleSpeed   = 0;
        self.percent:float = 0.0;
        self.offset:int  = 0;
        self.scale:int   = 0;


#    template <typename BaseType>
#    class GenericFactory;

# template <typename BaseType>
# friend class GenericFactory;
        
class HandlerBase():

    def enterSection(self, name:str, value:Configurable) -> None:
        pass

    def matchesUninitialized(self, name:str) -> bool:
        pass

    def item(self, name:str, value:Macro) -> None:
        pass

    def item(self, name:str, value:bool) -> None:
        pass

    #def item(self, name:str, value:int, minValue:int=0, maxValue:int = sys.maxsize) -> None:
    #    pass

    #def item(self, name:str, value:int, minValue:int = 0,  maxValue:int = sys.maxsize) -> None
    #    pass

    def item(self, name:str, value:int, minValue:int = 0, maxValue = sys.maxsize) -> None:
        int32_t v = int32_t(value);
        item(name, v, int32_t(minValue), int32_t(maxValue));
        value = uint8_t(v);


    def item(self, name:str, value:float, minValue:float = -3e38, maxValue:float = 3e38) -> None:
        pass

    def item(self, name:str, value:list[speedEntry]) -> None:
        pass

    def item(self, name:str, value:list[float]) -> None: 
        pass
    
    def item(self, name:str, wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        pass

    def item(self, name:str, value:Pin) -> None:
        pass

    def item(self, name:str, value:IPAddress) -> None:
        pass

    def item(self, name:str, value:int, e:EnumItem) -> None:
        pass

    def item(self, name:str, value:str, minLength:int = 0, maxLength:int = 255) -> None:
        pass

    def handlerType(self) -> HandlerType:
        pass

    #template <typename T, typename... U>

    def section(self, name:str, value:object, **kwargs) -> None:
        if (handlerType() == HandlerType.Parser):
            #// For Parser, matchesUninitialized(name) resolves to _parser.is(name)
            if (matchesUninitialized(name)):
                Assert(value == nullptr, "Duplicate section %s", name);
                value = new T(args...);
                enterSection(name, value);
        else: 
            if not value: 
                self.enterSection(name, value);

    #template <typename T>
    def enterFactory(self, name:str, value:object) -> None:
        self.enterSection(name, value)
