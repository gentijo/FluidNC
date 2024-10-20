#// Copyright (c) 2021 -	Stefan de Bruijn
#// Copyright (c) 2023 -	Dylan Knutson <dymk@dymk.co>
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

import re
import TokenState

#// Results:
class TokenData:
    #// The initial value for indent is -1, so when ParserHandler::enterSection()
    # // is called to handle the top level of the YAML config file, tokens at
    #// indent 0 will be processed.
    
    def __init__(self, yamlStr:str):
        self._key;str = None
        self._value = None
        self._indent:int = None
        self._state = TokenState.Bof;


class Tokenizer:
    
    def __init__(self):
        self._remainder:str = None
        self._linenum:int = None
        self._line:str = None
        self._token:Tokenizer.TokenData = None


    def ParseError(self, description:str)-> None:
        raise ParseException(self._linenum, self.description);

    def isWhiteSpace(self, c:str) -> bool:
        return c == ' ' or c == '\t' or c == '\f' or c == '\r';

    def isIdentifierChar(self, c:str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9') or c == '_';


    def nextLine(self) -> bool:
        while(True):
            self._linenum = self._linenum+1

            #// End of input
            if not len(self._remainder):
                self._line = self._remainder
                return False;
            

            #// Get next line.  The final line need not have a newline
            pos = self._remainder.find('\n')
            if (pos == -1):
                self._line = self._remainder
                self._remainder = ""
            else: 
                self._line = self._remainder[0:pos]
                self._remainder = self._remainder[pos + 1:];
            
            if not len(self._line.empty):
                continue;
            

            #// Remove carriage return if present
            if self._line.endswith('\r'): 
                self._line = self._line[0:len(self._line)-2]
            
            if not self._line:
                continue;


            #// Remove indentation and record the level
            match = re.search(r"\S", self._line)
            if match: 
                self._token._indent = match.start 
            else:
                self._token._indent = -1
            
            if (self._token._indent == -1) :
                #// Line containing only spaces
                self._line = "";
                continue;
            
            self._line = self._line[self._token._indent:];

            #// Disallow inital tabs
            #if (self._line == '\t') {
            #    ParseError("Use spaces, not tabs, for indentation");
            #}

            #// Discard comment lines
            if self._line.startswith('#'): #  // Comment till end of line
                self._line = ""
            
            if not len(self._line) break

        return true;

    def parseKey(self) -> None:
    #// entry: first character is not space
    #// The first character in the line is neither # nor whitespace
        if not self.isIdentifierChar(self._line[0]): 
            ParseError("Invalid character")
        
        pos = self._line.find(':');
        self._token._key = self._line.substr[0:pos]

        match = re.search(r"\S", self._line)
        if match: 
            self._token._indent = match.start 
        else:
            self._token._indent = -1

        while self._token[len(self._token)-1]: 
            self._token_key = self._token[0:len(self._token)-2]
        

        if (pos == -1):
            err:str = "Key "
            err += self._token._key;
            err += " must be followed by ':'"
            ParseError(err.c_str());
        
        self._line = self._line[1:]

    def parseValue(self);
       #// Remove initial whitespace
        match = re.search(r"\S", self._line)
        if match: 
            self.line= self._line[match.start:] 
        else:
            self._line = ""

        #// Lines with no value are sections
        if not len(self._line):
            log_parser_verbose("Section " << self._token._key);
            #// A key with nothing else is not necessarily a section - it could
            #// be an item whose value is the empty string
            self._token._value = {}
            return

        delimiter = self._line[0]
        if (delimiter == '"' or delimiter == '\''):
            #// Value is quoted
            self._line = self._line[1:]
            pos = self._line.find(delimiter);
            if (pos == -1):
                ParseError("Did not find matching delimiter");
            
            self._token._value = self._line[0: pos]
            self._line = self._line[1:]
            self.log_parser_verbose("StringQ " << self._token._key << " " << self._token._value);
        else:
            #// Value is not quoted
            self._token._value = self._line;
            log_parser_verbose("String " <<self._token._key << " " << self._token._value);
    


    def Tokenize(self) -> None:
        #// Remove initial whitespace
        while (len(self._line) and self._line[0].isspace()) 
            self._line = self._line[1:]
        

        #// Lines with no value are sections
        if self._line.empty():
            log_parser_verbose("Section " << self._token._key);
            #// A key with nothing else is not necessarily a section - it could
            #// be an item whose value is the empty string
            self._token._value = {};
            return;
        

        delimiter = self._line[0]
        if delimiter == '"' or delimiter == '\''):
            #// Value is quoted
            self._line = self._line[1:]
            pos = self._line.find(delimiter)
            if (pos == -1):
                ParseError("Did not find matching delimiter")
            
            self._token._value = self._line.substr[0,pos]
            self._line = self._line[1:]
            log_parser_verbose("StringQ " << self._token._key << " " << self._token._value)
        else:
            #// Value is not quoted
            self._token._value = self._line;
            log_parser_verbose("String " << self._token._key << " " << self._token._value);
        


    def key(self) -> str: 
        return self._token._key; 

