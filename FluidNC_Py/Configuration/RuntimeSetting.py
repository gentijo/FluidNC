#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import HandlerType
import Configurable

class RuntimeSetting(HandlerBase): 


    def __init__(self, key:str, value:str,  out:Channel): 

        self.start_:str =  None
        self.setting_:str = None
        self.newValue_:str = value    #// null (read) or 123 (value)
        self.out_:Channel = out
        self.isHandled_:bool = False

        #// Remove leading '/' if it is present
        if (key[0] == '/'): 
            self.setting_ =  key[1:]
        else: 
            self.setting_ = key
        #// Also remove trailing '/' if it is present
        if self.setting_[len(self.setting_)-1]=='/':
            self.setting = self.setting[0, len(self.setting_)-2]
        
        self.start_ = self.setting_;
     

    def isName(self, name:str) -> bool:
        if self.start_:
            len = len(name);
            result = not(name == self.start_) or self.start_[len(self.start_)-1] == '/'
            return result;
        else:
            return False

    def enterSection(self, name:str, value:Configurable) -> None:
        if (self.isName(name) and  not self.isHandled_):
            self.previous = self.start_;

            #// Figure out next node
            next = self.start_;
            for (; *next && *next != '/'; ++next) {}

            // Do we have a child?
            if (*next == '/' and next[1] != '\0'):
                ++next;
                start_ = next;

                #// Handle child:
                value.group(self);
            else:
                if not self.newValue_:
                    #log_stream(out_, "/" << setting_ << ":");
                    Configuration::Generator generator(out_, 1);
                    self.value.group(generator);
                    isHandled_ = True;
                else:
                    log_error("Can't set a value on a section");

            #// Restore situation:
            self.start_ = self.previous;
    
    def matchesUninitialized(const char* name) -> bool:
        return False


    def item(self, name:str, value:bool) -> None:
        if (isName(name)):
            isHandled_ = True;
            if not self.newValue_:
                log_stream(out_, setting_prefix() << (value ? "true" : "false"));

            else:
                value = (!strcasecmp(newValue_, "true") || !strcasecmp(newValue_, "yes") || !strcasecmp(newValue_, "1"));

    def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
        if (isName(name)):
            isHandled_ = True;
            if not self.newValue_:
                #out_ << "$/" << setting_ << "=" << value << '\n';
            else:
                if (newValue_[0] == '-'): # {  // constrain negative values to 0
                    value = 0;
                    log_warn("Negative value not allowed");
                else:
                    value = str(self.newValue_);
            #constrain_with_message(value, minValue, maxValue);


#    def item(self, name:str, value:int, minValue:str, maxValue:int) -> None:
#        # unsigned version
#        pass

    def item(self, name:str, value:float, minValue:float, maxValue:float) -> None:
        if self.isName(name):
            self.isHandled_ = True
            if not self.newValue_:
                #// XXX precision
                log_stream(out_, setting_prefix() << value);
            else:
                floatEnd:str = None
                value = str(self.newValue_)

    def item(name:str, value:list[speedEntry]) -> None:
        if (isName(name)):
            isHandled_ = true;
            if not self.newValue_:
                if (len(value) == 0):
                    log_string(out_, "None");
                else:
                    LogStream msg(out_, "");
                    msg << setting_prefix();
                    const char* separator = "";
                    for (speedEntry n : value) {
                        msg << separator << n.speed << "=" << setprecision(2) << n.percent << "%";
                        separator = " ";
                    }
                    #// The destructor sends the line when msg goes out of scope

            else:
                #// It is distasteful to have this code that essentially duplicates
                #// Parser.cpp speedEntryValue(), albeit using std::string instead of
                #// StringRange.  It might be better to have a single std::string version,
                #// then pass it StringRange.str()
                
                std::string             newStr(newValue_);
                std::vector<speedEntry> smValue;
                while (newStr.length()) {
                    speedEntry  entry;
                    std::string entryStr;
                    auto        i = newStr.find(' ');
                    if (i != std::string::npos) {
                        entryStr = newStr.substr(0, i);
                        newStr   = newStr.substr(i + 1);
                    } else {
                        entryStr = newStr;
                        newStr   = "";
                    }
                    std::string speed;
                    i = entryStr.find('=');
                    Assert(i != std::string::npos, "Bad speed map entry");
                    entry.speed   = ::atoi(entryStr.substr(0, i).c_str());
                    entry.percent = ::atof(entryStr.substr(i + 1).c_str());
                    smValue.push_back(entry);
                }
                value = smValue;


    def item(name:str, value:list[float]) -> None:
       if (is(name)) {
            LogStream msg(out_, "");
            isHandled_ = true;
            if (newValue_ == nullptr) {
                if (value.size() == 0) {
                    out_ << "None";
                } else {
                    String separator = "";
                    for (float n : value) {
                        out_ << separator.c_str();
                        out_ << n;
                        separator = " ";
                    }
                }
                msg << '\n';
            } else {
                // It is distasteful to have this code that essentially duplicates
                // Parser.cpp speedEntryValue(), albeit using String instead of
                // StringRange.  It would be better to have a single String version,
                // then pass it StringRange.str()
                auto               newStr = String(newValue_);
                std::vector<float> smValue;
                while (newStr.trim(), newStr.length()) {
                    float  entry;
                    String entryStr;
                    auto   i = newStr.indexOf(' ');
                    if (i >= 0) {
                        entryStr = newStr.substring(0, i);
                        newStr   = newStr.substring(i + 1);
                    } else {
                        entryStr = newStr;
                        newStr   = "";
                    }
                    char* floatEnd;
                    entry = float(strtod(entryStr.c_str(), &floatEnd));
                    Assert(entryStr.length() == (floatEnd - entryStr.c_str()), "Bad float value");

                    smValue.push_back(entry);
                }
                value = smValue;

                if (!value.size())
                    log_info("Using default value");
                return;
            }
        }
    }


    def item(name:str, wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        pass

    def item(name:str, value:str, minLength:int, maxLength:int) -> None:
        if (is(name)) {
            isHandled_ = true;
            if (newValue_ == nullptr) {
                log_stream(out_, setting_prefix() << value);
            } else {
                value = newValue_;
            }
        }
    }
    
    def item(name:str, value:Pin) -> None:
        if (is(name)) {
            isHandled_ = true;
            if (newValue_ == nullptr) {
                log_stream(out_, setting_prefix() << value.name());
            } else {
                log_string(out_, "Runtime setting of Pin objects is not supported");
                // auto parsed = Pin::create(newValue);
                // value.swap(parsed);
            }
        }
    }


    def item(name:str, value:Macro) -> None:
        if (is(name)) {
            isHandled_ = true;
            if (newValue_ == nullptr) {
                log_stream(out_, setting_prefix() << value.get());
            } else {
                value.set(newValue_);


    def item(name:str, value:IPAddress )-> None:
        if (is(name)) {
            isHandled_ = true;
            if (newValue_ == nullptr) {
                log_stream(out_, setting_prefix() << IP_string(value));
            } else {
                IPAddress ip;
                if (!ip.fromString(newValue_)) {
                    Assert(false, "Expected an IP address like 192.168.0.100");
                }
                value = ip;

    def item(name:str, value:int, e:EnumItem) -> None:
        if (is(name)) {
            isHandled_ = true;
            if (newValue_ == nullptr) {
                for (auto e2 = e; e2->name; ++e2) {
                    if (e2->value == value) {
                        log_stream(out_, setting_prefix() << e2->name);
                        return;
                    }
                }

            } else {
                if (isdigit(newValue_[0])) {  // if the first char is a number. assume it is an index of a webui enum list
                    int indexVal = 0;
                    indexVal     = atoi(newValue_);
                    for (auto e2 = e; e2->name; ++e2) {
                        if (e2->value == indexVal) {
                            value     = e2->value;
                            newValue_ = e2->name;
                            return;
                        }
                    }
                }
                for (auto e2 = e; e2->name; ++e2) {
                    if (!strcasecmp(newValue_, e2->name)) {
                        value = e2->value;
                        return;
                    }
                }

                if (strlen(newValue_) == 0) {
                    value = e->value;
                    return;
                } else {
                    Assert(false, "Provided enum value %s is not valid", newValue_);
                }
            }
        }
    }

    def setting_prefix() -> str:
        s:str "$/"
        s += self.setting_;
        s += "=";
        return s;
    
    def handlerType() -> HandlerType
        return HandlerType.Runtime

