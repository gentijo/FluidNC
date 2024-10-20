#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import Configurable
from  HandlerBase import HandlerBase, speedEntry

class Completer(HandlerBase):
        
    def __init__(self, key:str, requestedMatch:int, matchedStr:str ) -> None:
    
        self._key:str = KeyError
        self._reqMatch:int =requestedMatch
        self._matchedStr:str =  machedStr
        self._currentPath:str = "/"
        self.numMatches:int = 0

    def addCandidate(self, fullName:str) -> None:
        if ((self._matchedStr and self._numMatches) == self._reqMatch):
            self._matchedStr = fullName
        
        self._numMatches self._nmMatches+1

    
    def enterSection(self, name:str, value:Configurable) -> None:
        previous = self._currentPath
        self._currentPath += name;
        self._currentPath = self._currentPath + "/"

        if (self._key.rfind(self._currentPath) == 0):
            #// If _currentPath is an initial substring of _key, this section
            #// is part of a path leading to the key, so we have to check
            #// this section's children
            #// Example: _key = /axes/x/motor0/cy _currentPath=/axes/x/motor0
            value.group(self)

        elif (self._currentPath.rfind(self._key, 0) == 0):
            #// If _key is an initial substring of _currentPath, this section
            #// is a candidate.  Example:  _key = /axes/x/h _currentPath=/axes/x/homing
            self.addCandidate(self._currentPath)

        self._currentPath = previous


    def matchesUninitialized(self, name:str) -> bool:
        return False


    def item(self, name:str) -> None:
        fullItemName = self._currentPath + name
        if (fullItemName.rfind(self._key) == 0):
            self.addCandidate(fullItemName)
    
    def item(self, name:str, value:int) -> None:
        self.item(name); 

    def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
        self.item(name); 
        pass

    def item(self, name:str, value:int, minValue:int, maxValue:int) -> None:
        self.item(name); 
        pass

    def item(self, name:str, value:float, minValue:float, maxValue:float) -> None:
        self.item(name)

    def item(self, name:str, value:list) -> None:
        self.item(name); 

    def item(self, name:str, value:list) -> None:
        self.item(name); 

    def item(self, name:str, wordLength:UartData, parity:UartParity, stopBits:UartStop) -> None:
        self.item(name); 

    def item(self, name:str, value:str, minLength:int, maxLength:int) -> None: 
        self.item(name); 

    def item(self, name:str, value:Pin) -> None:
        self.item(name);

    def item(self, name:str, value: Macro) -> None:
        self.item(name); 

    def item(name:str, value:IPAddress) -> None: 
        self.item(name); 
    
    def item(name:str, value:int, e:EnumItem) -> None:
        self.item(name); 

    def handlerType(self) -> HandlerType:
        return HandlerType.Completer; 

def isInitialSubstringCI(self, key:str, test:str) -> bool:
    while (key and test):
        if (tolower(*key++) != tolower(*test++)):
            return false;
        
    return *key == '\0'

#// This provides the interface to the completion routines in lineedit.cpp
#// The argument signature is idiosyncratic, based on the needs of the
#// Forth implementation for which the completion code was first developed.
##//
#// key, keylen is the address and length of an array of bytes, not null-terminated,
#//    for which we seek matches.
#// matchnum is the index of the match that we will return
#// matchname is the matchnum'th match

def num_initial_matches(key:str, keylen:int, matchnum:int, matchname:str)->  int:

    nfound:int = 0;

    if (key[0] == '/'):
        keycstr:str = key

        #// Match in configuration tree
        Configuration::Completer completer(keycstr, matchnum, matchname)
        config->group(completer)
        nfound = completer._numMatches
    else:
        #// Match NVS settings
        for (Setting* s : Setting):
            if (isInitialSubstringCI(key, s->getName())):
                if (matchname and nfound == matchnum):
                    strcpy(matchname, s->getName());
                
                ++nfound;

    return nfound;
