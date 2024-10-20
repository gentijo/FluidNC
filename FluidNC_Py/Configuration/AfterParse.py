#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import Configurable
import HandlerType

class AfterParse(HandlerBase):

    #AfterParse(const AfterParse&) = delete;
    #AfterParse& operator=(const AfterParse&) = delete;

    def __init__(self):
        self._path:list = []

    def enterSection(self, name:str, value:Configurable) -> None:
        self._path.append(name);  #// For error handling

        try:
            self.value.afterParse();
        except: Exception as ex:
            #// Log something meaningful to the user:
            #log_config_error("Initialization error at "; for (auto it : _path) { ss << '/' << it; } ss << ": " << ex.msg);
            self.value.group(self)

        #self._path.erase(_path.begin() + (_path.size() - 1));
    

    def matchesUninitialized(self, name:str) -> bool:
        return False; 

    def handlerType(self) -> HandlerType:
        return HandlerType.AfterParse; 


    def item(self, name:str, value:bool) -> None:
        pass

    def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
        pass

    def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
        pass

    def item(self, name:str, value:float, minValue:float, maxValue:float) -> None:
        pass

    def item(self, name:str, value:list) -> None:
        pass

    def item(self, name:str, value:list) -> None:
        pass

    def item(self, name:str, wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        pass

    def item(self, name:str, value:str, minLength:int, maxLength:int) -> None:
        pass

    def item(self, name:str, value:Pin)  -> None:
        pass

    def item(self, name:str, value:Macro) -> None:
        pass

    def item(self, name:str, value:IPAddress) -> None:
        pass

    def item(self, name:str, value, e:EnumItem) -> None:
        pass


