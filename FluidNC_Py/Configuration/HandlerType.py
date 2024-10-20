#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

from enum import Enum

class HandlerType(Enum):
    Parser=1
    AfterParse=2 
    Runtime=3 
    Generator=4 
    Validator=5 
    Completer=6

