#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.
from multipledispatch import dispatch

class Configurable

class JsonGenerator(HandlerBase):
        
#    JsonGenerator(const JsonGenerator&)            = delete;
#    JsonGenerator& operator=(const JsonGenerator&) = delete;

    def __init__(self):
        self._currentPath:str = ""
        self._depth:int       = 0
        self._paths:list = []
        self._paths.append(self._currentPath)
    

    def enter(self, name:str) -> None:
        currentEnd = self._paths[self._depth]
        currentEnd = '/'
    
#        for (i = name; i):
#            assert(currentEnd != _currentPath + 256, "Path out of bounds while serializing json.");
#            currentEnd = currentEnd+1    
#        self._depth = self._depth+1
#        self._paths[self._depth] = currentEnd;
#        currentEnd    = ""


    def add(self, configurable:Configurable):
        if configurable:
            configurable.group(self)
        

    def leave(self)->None:
        self._depth = self._depth-1
#        Assert(_depth >= 0, "Depth out of bounds while serializing to json");
        self._paths[self._depth] = ""
    
    def enterSection(self, name:str, value:Configurable) -> None:
        self.enter(name)
        value.group(self)
        self.leave()


    def matchesUninitialized(const char* name) -> bool:
        return false
    
#    HandlerType handlerType() override { return HandlerType::Generator; }
#    explicit JsonGenerator(JSONencoder& encoder);


    @multimethod(str, bool)
    def item(self, name:str, value:bool) -> None:
        self.enter(name)

        val:str = "0" 
        if value: 
            val = "1"

        self._encoder.begin_webui(self._currentPath, self._currentPath, "B", val)
        self._encoder.begin_array("O")
        
        self._encoder.begin_object()
        self._encoder.member("False", 0)
        self._encoder.end_object()
        self._encoder.begin_object()
        self._encoder.member("True", 1)
        self._encoder.end_object()
        
        self._encoder.end_array()
        self._encoder.end_object();
        self.leave();
    

# This is probably the unsigned version
#    @item.dispatch(str, int, int, int)
#    def item(name:str, value:int, minValue:int, maxValue:int):
#        self.enter(name);
#    
#        buf:str = str(value)
#        self._encoder.begin_webui(self._currentPath, self._currentPath, "I", buf, minValue, maxValue);
#        self._encoder.end_object();
#    
#        self.leave();
    
    

    @item.dispatch(str, int, int, int)
    def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
        self.enter(name);
        
        buf:str = str(value)
        self._encoder.begin_webui(self._currentPath, self._currentPath, "I", buf, minValue, maxValue);
        self._encoder.end_object();
        self.leave();
    
    @item.dispatch(object, str, float, float, float)
    def item(self, name:str, value:float, minValue:float, maxValue:float) -> None:

        self.enter(name)
        #// WebUI does not explicitly recognize the R type, but nevertheless handles it correctly.
        if value > 999999.999 :
            value = 999999.999
        elif value < -999999.999:
            value = -999999.999
        
       
        fstr =f"{value:.2f}"
        self._encoder.begin_webui(self._currentPath, self._currentPath, "R", fstr);
        self._encoder.end_object();
        self.leave();


    def item(self, name:str, value:list) -> None: 
        pass

    def item(name:str, value:list) -> None:
        pass


    def item(self, name:str, wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        #// Not sure if I should comment this out or not. The implementation is similar to the one in Generator.h.
        pass

    def item(self, name:str, value:str, minLength:int, maxLength:int) -> None:
        self.enter(name)
        self._encoder.begin_webui(self._currentPath, self._currentPath, "S", value.c_str(), minLength, maxLength)
        self._encoder.end_object()
        self.leave()
    

    def item(self, name:str, value:Macro) -> None
        self.enter(name)
        self._encoder.begin_webui(self._currentPath, self._currentPath, "S", value, 0, 255)
        self._encoder.end_object()
        self.leave()
    
    def item(self, name:str, value:Pin) -> None:
        #// We commented this out, because pins are very confusing for users. The code is correct,
        #// but it really gives more support than it's worth.
        #/*
        #enter(name);
        #auto sv = value.name();
        #_encoder.begin_webui(_currentPath, _currentPath, "S", sv.c_str(), 0, 255);
        #_encoder.end_object();
        #leave();
        #*/
        pass

    def item(self, name:str, value:IPAddress) -> None:
        self.enter(name)
        self._encoder.begin_webui(self._currentPath, self._currentPath, "A", IP_string(value));
        self._encoder.end_object();
        self.leave();
    

    def item(self, name:str, value:int, e:EnumItem) -> None:
        self.enter(name);
        selected_val:int = 0;
        #//const char* str          = "unknown";
        
        for (e2 = e; e2.name):
            if value == e2->value:
                #//str          = e2->name;
                selected_val = e2.value
                break

        self._encoder.begin_webui(self._currentPath, self._currentPath, "B", selected_val);
        self_encoder.begin_array("O");
        for (e2 = e; e2.name; e2) {
            self._encoder.begin_object();
            self._encoder.member(e2.name, e2.value)
            self_encoder.end_object();
        
        self._encoder.end_array();
        self._encoder.end_object();
        self.leave();
    


