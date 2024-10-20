#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.


import Configurable;

class Validator(HandlerBase): 
#        Validator(const Validator&) = delete;
#        Validator& operator=(const Validator&) = delete;

    def __init__(self):
        self._path:list = []


    def enterSection(self, name:str, value:Configurable) -> None:
        self._path.append(name)  #// For error handling

        try: 
            value.validate();
        except Exception as e:
            pass
            #// Log something meaningful to the user:
            #log_config_error("Validation error at "; for (auto it : _path) { ss << '/' << it; } ss << ": " << ex.msg);
    
        #value->group(*this);

        #_path.erase(_path.begin() + (_path.size() - 1));



    def matchesUninitialized(self, name:str) -> bool:
        return False
    
    # HandlerType handlerType() override { return HandlerType::Validator; }


    #void item(const char* name, bool& value) override {}
    #void item(const char* name, int32_t& value, const int32_t minValue, const int32_t maxValue) override {}
    #void item(const char* name, uint32_t& value, const uint32_t minValue, const uint32_t maxValue) override {}
    #void item(const char* name, float& value, const float minValue, const float maxValue) override {}
    #void item(const char* name, std::vector<speedEntry>& value) override {}
    #void item(const char* name, std::vector<float>& value) override {}
    #void item(const char* name, UartData& wordLength, UartParity& parity, UartStop& stopBits) override {}
    #void item(const char* name, std::string& value, const int minLength, const int maxLength) override {}
    #void item(const char* name, Pin& value) override {}
    #void item(const char* name, Macro& value) override {}
    #void item(const char* name, IPAddress& value) override {}
    #void item(const char* name, int& value, const EnumItem* e) override {}
