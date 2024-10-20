#// Copyright (c) 2021 -	Stefan de Bruijn
#// Use of this source code is governed by a GPLv3 license that can be found in the LICENSE file.

from HandlerBase import HandlerBase
 
class Configurable:
        #Configurable(const Configurable&) = delete;
        #Configurable(Configurable&&)      = default;

        #Configurable& operator=(const Configurable&) = delete;
        #Configurable& operator=(Configurable&&) = default;

        #Configurable() = default;

    def validate() -> None:
        pass


    def group(handler:HandlerBase) -> None:
        pass

    def afterParse() -> None:
        pass
