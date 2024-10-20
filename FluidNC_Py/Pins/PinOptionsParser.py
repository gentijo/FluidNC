#// Copyright (c) 2021 -  Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.


#// Pin options are passed as PinOption object. This is a simple C++ forward iterator,
#// which will implicitly convert pin options to lower case, so you can simply do
#// stuff like this:
#//
#// for (auto it : options) {
#//   const char* currentOption = it();
#//   ...
#//   if (currentOption.is("pu")) { /* configure pull up */ }
#//   ...
#// }
#//
#// This is a very light-weight parser for pin options, configured as 'pu:high:etc'
#// (full syntax f.ex.: gpio.12:pu:high)
#

# class PinOptionsParser;

class PinOption():

    def __init__(self):
        self._option:str  = None
        self._key:str     = None
        self._value:str   = None
        self._options:str = None

    def PinOption(self, options:str) -> None:
        self._options = options
        self.tokenize()

    def tokenize(self) -> None:
        if not len(self._options):
            _option = _key = _value = {};
            return;
        
        pos = self._options.find(":;");
        _option  = self._options[0:pos];

        if pos == -1:
            self._option = self._options;
            self._options=""
        else:
            self._option = self._options[0:pos]
            self._options[pos+1:]

        pos = _option.find('=')
        if (pos == -1):
            self._key   = _option
            self._value = {}
        else:
            self._key   = _option[0:pos]
            self._value = _option.substr(pos + 1)


    def isOption(self, option:str) -> bool:
        return self._key.lower() == option.lower()

    def iValue(self) -> int:
        if (self._value):
            return int(self._value)
        return None

    #inline const std::string_view operator()() { return _option; }

    def value(self) ->str:
        return self.value
    
    def key(self) -> str:
        return self._key

    #// Iterator support:
    #inline PinOption const* operator->() const { return this; }
    #inline PinOption        operator*() const { return *this; }
    #PinOption&              operator++();

    def __eq__(self, o:PinOption) -> bool:
            return self._key.lower() == o._key.lower()
    
    def __ne__(self, o:PinOption& o) -> bool:
        return self._key.lower() != o._key.lower() 

    def next(self) -> PinOption:
        self.tokenize();
        return self;
    
    # // This parses the options passed to the Pin class.
    # class PinOptionsParser {
    #     std::string_view _options;

    # public:
    #     PinOptionsParser(std::string_view options);

    #     inline PinOption begin() const { return PinOption(_options); }
    #     inline PinOption end() const { return PinOption(std::string_view()); }
