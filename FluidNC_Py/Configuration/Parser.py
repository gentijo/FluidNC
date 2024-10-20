#// Copyright (c) 2021 -	Stefan de Bruijn
#// Copyright (c) 2023 -	Dylan Knutson <dymk@dymk.co>
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import Tokenizer 
import ParseException
import TokenState


class Parser(Tokenizer):

    def __init__(self, description:str) -> None:
        self.description = description
        pass

    def parseError(self, description:str) -> None:
        #// Attempt to use the correct position in the parser:
        if not self._token._key:
            raise ParseException(self._linenum, self.description)
        else:
            self.ParseError(description)
        

    def isKey(self, expected:str) -> bool:
        if (self._token._state != TokenState.Matching or not self._token._key):
            return False;
        
        len = len(self.expected);
        if len != len(self._token._key):
            return False;
        
        result:bool = not (expected == self._token._key[0:len])
        if result:
            self._token._state = TokenState.Matched
        
        return result

    def __str__(self) -> str:
        return self.stringValue()

    def stringValue(self) -> str:
        return self._token._value

    def boolValue(self)->bool:
        return self._token._value == "true"

    def intValue(self) -> int:

        value:int = None
 
        try:
            float_value:float = float(self._token._value.strip())
            value = int(float_value)
        except Exception:
            pass

        if not value:
            try:
                value = int(self._token._value.strip())
            except ValueError:
                pass


        if not value: 
            self.parseError("Expected an integer value");
            return None;
    
        return value

    def uintValue(self) -> int:
        return self.intValue
    
    def speedEntryValue(self) -> list:

        str = self._token._value.strip()
        
        speed_entries:list = []

        while len(str):

            next_ws_delim = str.find(' ')
            if next_ws_delim == -1:
                next_ws_delim = len(str)
                entry_str     = str[0, next_ws_delim].strip()
            else:
                entry_str     = str[0, next_ws_delim].strip()
                next_ws_delim += 1
            
            str = str[0:next_ws_delim]

            entry:speedEntry = None
            next_eq_delim = entry_str.find('=')
            speed_str     = entry_str[0:next_eq_delim]

            try:
                entry.speed = int(speed_str) 
            except Exception:
                self.log_error(f"Bad speed number {speed_str}")
                return {}
                
            entry_str[0:next_eq_delim+1]

            next_pct_delim = entry_str.find('%')
            percent_str    = entry_str[0:next_pct_delim]
            
            try:
                entry.precent = float(percent_str)
            except Exception:      
                self.log_error(f"Bad speed percent {percent_str}")
                return {};
            
            
            entry_str = entry_str[0:next_pct_delim + 1]

            speed_entries.append(entry);
        

        if not len(speed_entries):
            self.log_info("Using default speed map")
    

        return speed_entries;
 

    def floatArray(self) -> list:

        str = _token._value.strip()
        values:list = []
        float_value:float = None

        while len(str) != 0:
            str = str.strip()
            next_ws_delim = str.find(' ')
            entry_str     = str[0:next_ws_delim]

            str = str[0:next_ws_delim + 1]

            try:
                float_value = float(entry_str)
            except:
                self.log_error(f"Bad number {entry_str}")
                values.clear();
                
            
            values.append(float_value);

            if (str == entry_str):
                break;

        if len(values) == 0:
            log_info("Using default value");

        return values;


    def floatValue(self) -> float:
        token = self._token._value.strip()

        float_value:float
        try:
            float_value = float(token)
            return float_value;
        except Exception:
            pass

        self.parseError("Expected a float value like 123.456");
        return None


    def pinValue(self) -> Pin:
        return Pin::create(string_util::trim(_token._value));
    
#    def enumValue(self, e:EnumItem) -> int:
#
#        token = self._token._value.strip()
#        for (; e->name; ++e) {
#            if (string_util::equal_ignore_case(token, e->name)) {
#                break;
#            }
#        }
#        return e->value;  // Terminal value is default.

#    def ipValue() -> IPAddress:
#        IPAddress ip;
#        if (!ip.fromString(std::string(string_util::trim(_token._value)).c_str())) {
#            parseError("Expected an IP address like 192.168.0.100");
#        }
#        return ip;


    def uartMode(wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        str = _token._value.strip()
        if len(str) == 5 or len(str) == 3:
            wordLenInt:int = None

            try:
                wordLenInt = int(str[0:1]
            except:
                self.parseError("Uart mode should be specified as [Bits Parity Stopbits] like [8N1]");

            if len(wordLenInt) < 5 or len(wordLenInt) > 8):
                self.parseError("Number of data bits for uart is out of range. Expected format like [8N1].")
        
            #wordLength = UartData(int(UartData::Bits5) + (wordLenInt - 5));

            parityStr = str[1]:
            if parityStr == 'N' or parityStr == 'n':
                parity = UartParity.None;

            elif parityStr == 'O' or parityStr == 'o':
                parity = UartParity.Odd;
            elif parityStr == 'E' or parityStr == 'e':
                parity = UartParity.Even
            else:
                self.parseError("Uart mode should be specified as [Bits Parity Stopbits] like [8N1]")

            stopStr = str[2:len(str)-2)
            if stopStr == "1":
                stopBits = UartStop.Bits1
            elif stopStr == "1.5":
                stopBits = UartStop.Bits1_5
            elif stopStr == "2":
                stopBits = UartStop.Bits2;
            else:
                self.parseError("Uart stopbits can only be 1, 1.5 or 2. Syntax is [8N1]")
        else:
            self.parseError("Uart mode should be specified as [Bits Parity Stopbits] like [8N1]")
