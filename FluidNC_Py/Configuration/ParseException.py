#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.


class ParseException(Exception):
    def __init__(self, **kwargs):
        self._linenum = 0;
        self._description:str = None
        if "ParseException" in kwargs:
            pex:ParseException = kwargs["ParseException"]
            if pex:
                self._linenum = pex._linenum
                self._description = pex._description

        if "Description" in kwargs:
            str = kwargs["Description"]
            if (str):
                self._description = str

        if "Linenum" in kwargs:
            str = kwargs["Linenum"]
            if (str):
                self._linenum = kwargs["Linenum"]


    def LineNumber(self) -> int:
        return self._linenum
    
    def What(self) -> str:
        return self._description; 
