#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import LegacySettingHandler;


class LegacySettingRegistry:
        static LegacySettingRegistry& instance() {
            static LegacySettingRegistry instance_;
            return instance_;
        }

#    LegacySettingRegistry(const LegacySettingRegistry&) = delete;
#    LegacySettingRegistry& operator=(const LegacySettingRegistry&) = delete;

    self.handlers_:list[LegacySettingHandler]



    def isLegacySetting(self, s:str) -> bool:
        return str[0] == '$' and (str[1] >= '0' and str[1] <= '9');
    

    def registerHandler(handler:LegacySettingHandler() -> None:
        self.handlers_.append(handler)
    

    #// cppcheck-suppress unusedFunction
    bool tryHandleLegacy(s:str) -> bool:

        indx:int = 0;

        if isLegacySetting(s):
            start:str = s
            value:int = 0;
            ++indx;

            while (s[indx] and s[indx] >= '0' and str[indx] <= '9'):
                value = value * 10 + (*str - '0');
                indx++
            

            if (str[indx] == '='):
                ++indx

                tryLegacy(value, str);
            else:
                log_warn(f"Incorrect setting {start} : cannot find '='");
            
            return True;
        else:
            return False;
        

    def tryLegacy(self, index:int, value:str):
        handled:bool = false;
        
        for (it in self.handlers_ ):
            if it->index() == index:
                handled = true;
                it->setValue(value);
                #// ??? Show we break here, or are index duplications allowed?

        if not handled:
            log_warn(f"Cannot find handler for $ {index}. Setting was ignored.");
