#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import HandlerBase
import Configurable

class Generator(HandlerBase):
        
#    Generator(const Generator&)            = delete;
#    Generator& operator=(const Generator&) = delete;

    def __init__(self):
        self.indent_:int = Mone
        self.dst_:Channel = None
        self.lastIsNewline:bool_ = False

    def indent() -> None:
        lastIsNewline_ = false;
        for (int i = 0; i < indent_ * 2; ++i) {
            dst_ << ' ';


    void enter(const char* name);
    void add(Configuration::Configurable* configurable);
    void leave();

    void        enterSection(const char* name, Configurable* value) override;
    bool        matchesUninitialized(const char* name) override { return false; }
    HandlerType handlerType() override { return HandlerType::Generator; }

    Generator(Channel& dst, int indent = 0);

    void send_item(const char* name, const std::string& value):
        LogStream s(dst_, "");
        lastIsNewline_ = false;

        for (int i = 0; i < indent_ * 2; ++i):
            s << ' ';
        
        s << name;
        s << ": ";

        #// If value contains a colon, wrap text as string
        if (value.find(':') == std::string::npos):
            s << value;
        else:
            s << "'";
            s << value;
            s << "'";
        

    void item(const char* name, int& value, const int32_t minValue, const int32_t maxValue) override {
        send_item(name, std::to_string(value));
    }

    void item(const char* name, uint32_t& value, const uint32_t minValue, const uint32_t maxValue) override {
        send_item(name, std::to_string(value));
    }

    void item(const char* name, float& value, const float minValue, const float maxValue) override {
        send_item(name, std::to_string(value));
    }

    void item(const char* name, std::vector<speedEntry>& value) {
        if (value.size() == 0) {
            send_item(name, "None");
        } else {
            std::ostringstream s;
            s.precision(2);
            const char* separator = "";
            for (speedEntry n : value) {
                s << separator << n.speed << "=" << std::fixed << n.percent << "%";
                separator = " ";
            }
            send_item(name, s.str());
        }
    }

    void item(const char* name, std::vector<float>& value) {
        if (value.size() == 0) {
            send_item(name, "None");
        } else {
            std::ostringstream s;
            s.precision(3);
            s << std::fixed;
            const char* separator = "";
            for (float n : value) {
                s << separator << n;
                separator = " ";
            }
            send_item(name, s.str());
        }
    }

    def item(name:str, wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        
        s:str = None
        s += f"{(int(wordLength) - int(UartData.Bits5) + 5)}";
        
        switch (parity) {
            case UartParity.Even:
                s += 'E';
                break;
            case UartParity.Odd:
                s += 'O';
                break;
            case UartParity.None:
                s += 'N';
                break;
        }
        switch (stopBits) {
            case UartStop.Bits1:
                s += '1';
                break;
            case UartStop.Bits1_5:
                s += "1.5";
                break;
            case UartStop.Bits2:
                s += '2';
                break;
        }
        send_item(name, s);
    }

    void item(const char* name, std::string& value, const int minLength, const int maxLength) override { send_item(name, value); }

    void item(const char* name, bool& value) override { send_item(name, value ? "true" : "false"); }

    void item(const char* name, Pin& value) override { send_item(name, value.name()); }
    void item(const char* name, Macro& value) override { send_item(name, value.get()); }

    void item(const char* name, IPAddress& value) override { send_item(name, IP_string(value)); }
    void item(const char* name, int& value, const EnumItem* e) override {
        const char* str = "unknown";
        for (; e->name; ++e) {
            if (value == e->value) {
                str = e->name;
                break;
            }
        }
        send_item(name, str);
    